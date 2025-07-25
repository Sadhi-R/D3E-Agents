import re
import asyncio
from file_manager import create_or_update_file
from sync_manager import update_code, Context
from config import remote_config

def save_components_from_d3e_output(d3e_output, project):
    """Extract and save D3E components in the specified project's folders."""
    component_types = ['Model', 'OptionSet', 'Widget', 'Page', 'Style', 'Theme', 'StyleTheme']
    d3e_type_map = {
        'model': 'Model',
        'optionset': 'OptionSet',
        'widget': 'Widget',
        'page': 'Page',
        'style': 'Style',
        'theme': 'StyleTheme',
        'styletheme': 'StyleTheme'
    }
    ctx = Context(remote_config)
    components_found = 0
    processed = set()
    def extract_component_blocks_improved(text, component_type):
        blocks = []
        patterns = [
            rf'{component_type}\s*\{{',
            rf'{component_type}\s+\{{',
            rf'{component_type.lower()}\s*\{{',
            rf'{component_type.lower()}\s+\{{',
            rf'\(\s*{component_type}\s+\w+\s*\)\s*\{{',
            rf'\(\s*{component_type.lower()}\s+\w+\s*\)\s*\{{',
            rf'\(\s*{component_type}\s+"[^"]+"\s*\)\s*\{{',
            rf'\(\s*{component_type.lower()}\s+"[^"]+"\s*\)\s*\{{',
            rf'\(\s*{component_type}\s+\'[^"]+\'\s*\)\s*\{{',
            rf'\(\s*{component_type.lower()}\s+\'[^"]+\'\s*\)\s*\{{',
            rf'\(\s*{component_type}\s*\)\s*\{{',
            rf'\(\s*{component_type.lower()}\s*\)\s*\{{',
        ]
        for pattern in patterns:
            regex = re.compile(pattern, re.MULTILINE | re.IGNORECASE)
            for match in regex.finditer(text):
                start = match.start()
                brace_count = 0
                i = start
                while i < len(text):
                    if text[i] == '{':
                        brace_count += 1
                    elif text[i] == '}':
                        brace_count -= 1
                        if brace_count == 0:
                            block = text[start:i+1]
                            blocks.append(block)
                            break
                    i += 1
        return blocks
    def extract_name_from_block_improved(block):
        name_patterns = [
            r"name\s*['\"]([^'\"]+)['\"]",
            r"name\s*:\s*['\"]([^'\"]+)['\"]",
            r"name\s*=\s*['\"]([^'\"]+)['\"]",
            r"['\"]name['\"]:\s*['\"]([^'\"]+)['\"]",
        ]
        for pattern in name_patterns:
            match = re.search(pattern, block, re.IGNORECASE)
            if match:
                return match.group(1)
        return None
    for component_type in component_types:
        blocks = extract_component_blocks_improved(d3e_output, component_type)
        for i, block in enumerate(blocks):
            name = extract_name_from_block_improved(block)
            if not name:
                name = f"{component_type.lower()}_generated_{i+1}"
            key = (component_type.lower(), name)
            if key in processed:
                continue
            processed.add(key)
            if not project:
                print("❌ Project must be specified for saving components.")
                continue
            success = create_or_update_file(component_type.lower(), name, block, project=project)
            if success:
                components_found += 1
                d3e_type = d3e_type_map[component_type.lower()]
                try:
                    sync_success, sync_message = asyncio.run(update_code(ctx, d3e_type, name, block))
                    status = "✅ SYNCED" if sync_success else "❌ SYNC FAILED"
                    print(f"{status} {name} ({d3e_type})")
                except Exception as e:
                    print(f"❌ SYNC FAILED {name} - Error: {str(e)}")
    if components_found == 0:
        print("⚠️ No D3E components found in AI output")