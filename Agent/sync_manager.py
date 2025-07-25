import os
import asyncio
import aiohttp
import threading
import time
from config import remote_config
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# Component types and their directory mapping
DIR_TYPE_MAP = {
    'Pages': 'Page',
    'Widgets': 'Widget',
    'Model': 'Model',
    'Style': 'Style',
    'StyleTheme': 'StyleTheme',
    'OptionSets': 'OptionSet'
}

# All component directories to watch for .d3e files
SYNC_DIRS = ['Pages', 'Widgets', 'Model', 'Style', 'StyleTheme', 'OptionSets']

# Set BASE_DIR to the project root
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

class Context:
    def __init__(self, login):
        self.login = login

async def update_code(ctx, type_, name, content):
    body = [
        {
            'type': type_,
            'identity': name,
            'code': content,
            'changeType': 'Update'  # Always use Update - the server will create if needed
        }
    ]
    url = f"{ctx.login['server']}/api/studioai/save-code?sessionId={ctx.login['sessionId']}"
    headers = {'Content-Type': 'application/json'}
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=body, headers=headers) as resp:
                if resp.status == 200:
                    return True, "SUCCESS"
                else:
                    text = await resp.text()
                    return False, f"HTTP {resp.status}: {text}"
    except Exception as e:
        return False, f"Exception: {str(e)}"

def find_d3e_files(project):
    """Find all D3E files in the project directory."""
    files = []
    base_dir = get_base_dir(project)  # Project is required
    for base in SYNC_DIRS:
        dir_path = os.path.join(base_dir, base)
        if os.path.isdir(dir_path):
            for fname in os.listdir(dir_path):
                if fname.endswith('.d3e'):
                    files.append((os.path.join(dir_path, fname), base))
    return files

async def sync_all_d3e_files(project):
    """Sync all .d3e files in the specified project."""
    ctx = Context(remote_config)
    files = find_d3e_files(project=project)
    if not files:
        return
    for fpath, base in files:
        d3e_type = DIR_TYPE_MAP.get(base)
        if not d3e_type:
            continue
        name = os.path.splitext(os.path.basename(fpath))[0]
        try:
            with open(fpath, 'r', encoding='utf-8') as f:
                content = f.read()
            success, message = await update_code(ctx, d3e_type, name, content)
            status = "✅ SYNCED" if success else "❌ FAILED"
            print(f"{status} {name} ({d3e_type})")
        except Exception as e:
            print(f"❌ FAILED {name} - Error: {str(e)}")

def get_base_dir(project=None):
    if project:
        return os.path.join(BASE_DIR, 'Projects', project)
    return BASE_DIR

class D3EFileChangeHandler(FileSystemEventHandler):
    def __init__(self, ctx, debounce_seconds=2.0):
        super().__init__()
        self.ctx = ctx
        self.debounce_seconds = debounce_seconds
        self._last_synced = {}  # file path -> last sync time
        self._sync_cache = {}   # file path -> last content hash
        self._lock = threading.Lock()
        
    def _get_file_hash(self, content):
        import hashlib
        return hashlib.md5(content.encode()).hexdigest()

    def _should_sync(self, fpath):
        try:
            with open(fpath, 'r', encoding='utf-8') as f:
                content = f.read()
                current_hash = self._get_file_hash(content)
        except Exception:
            return False

        now = time.time()
        with self._lock:
            last = self._last_synced.get(fpath, 0)
            last_hash = self._sync_cache.get(fpath)
            
            # Don't sync if content hasn't changed
            if current_hash == last_hash:
                return False
                
            # Don't sync if not enough time has passed
            if now - last < self.debounce_seconds:
                return False
                
            self._last_synced[fpath] = now
            self._sync_cache[fpath] = current_hash
            return True

    def on_modified(self, event):
        if event.is_directory:
            return
        if event.src_path.endswith('.d3e'):
            if self._should_sync(event.src_path):
                self.sync_file(event.src_path)

    def on_created(self, event):
        if event.is_directory:
            return
        if event.src_path.endswith('.d3e'):
            if self._should_sync(event.src_path):
                self.sync_file(event.src_path)

    def sync_file(self, fpath):
        base_dir = get_base_dir()
        rel_path = os.path.relpath(fpath, base_dir)
        for base in SYNC_DIRS:
            if rel_path.startswith(base):
                d3e_type = DIR_TYPE_MAP.get(base)
                if not d3e_type:
                    return
                name = os.path.splitext(os.path.basename(fpath))[0]
                try:
                    with open(fpath, 'r', encoding='utf-8') as f:
                        content = f.read()
                    print(f"[Watcher] Detected change in {fpath}, syncing...")
                    success, message = asyncio.run(update_code(self.ctx, d3e_type, name, content))
                    status = "✅ SYNCED" if success else "❌ FAILED"
                    print(f"[Watcher] {status} {name} ({d3e_type})")
                except Exception as e:
                    print(f"[Watcher] ❌ FAILED {name} - Error: {str(e)}")
                break

def start_file_watcher(project):
    """Start watching project's .d3e files for changes."""
    ctx = Context(remote_config)
    event_handler = D3EFileChangeHandler(ctx)
    observer = Observer()
    base_dir = get_base_dir(project=project)
    for base in SYNC_DIRS:
        dir_path = os.path.join(base_dir, base)
        if os.path.isdir(dir_path):
            observer.schedule(event_handler, dir_path, recursive=False)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join() 