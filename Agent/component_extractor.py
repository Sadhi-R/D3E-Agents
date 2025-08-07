import re
import json
import asyncio
from file_manager import create_or_update_file
from sync_manager import update_code, Context
from config import remote_config

def save_components_from_d3e_output(d3e_output, project):
    """Extract and save D3E components in the specified project's folders."""
    ctx = Context(remote_config)
    components_found = 0
    
    # First try to parse as JSON (new format)
    try:
        # Remove any markdown code block markers
        cleaned_output = d3e_output.strip()
        if cleaned_output.startswith('```json'):
            cleaned_output = cleaned_output[7:]
        if cleaned_output.startswith('```'):
            cleaned_output = cleaned_output[3:]
        if cleaned_output.endswith('```'):
            cleaned_output = cleaned_output[:-3]
        cleaned_output = cleaned_output.strip()
        
        # Try to parse as JSON
        components = json.loads(cleaned_output)
        
        # Handle both single component and array of components
        if not isinstance(components, list):
            components = [components]
            
        for component in components:
            if not isinstance(component, dict) or 'name' not in component:
                continue
                
            name = component['name']
            component_type = 'widget'  # Default to widget for JSON components
            
            # Determine component type based on content
            if 'fields' in component:
                component_type = 'model'
            elif 'buildTree' in component or 'properties' in component:
                component_type = 'widget'
            elif 'pages' in component:
                component_type = 'page'
            
            if not project:
                print("❌ Project must be specified for saving components.")
                continue
                
            # Convert back to JSON string for saving
            component_content = json.dumps([component], indent=4)
            
            success = create_or_update_file(component_type, name, component_content, project=project)
            if success:
                components_found += 1
                d3e_type_map = {
                    'model': 'Model',
                    'optionset': 'OptionSet',
                    'widget': 'Widget',
                    'page': 'Page',
                    'style': 'Style',
                    'theme': 'StyleTheme'
                }
                d3e_type = d3e_type_map[component_type]
                try:
                    # Use asyncio.create_task instead of asyncio.run to avoid event loop conflict
                    import asyncio
                    import threading
                    
                    def run_sync_in_thread():
                        try:
                            new_loop = asyncio.new_event_loop()
                            asyncio.set_event_loop(new_loop)
                            sync_success, sync_message = new_loop.run_until_complete(update_code(ctx, d3e_type, name, component_content))
                            status = "✅ SYNCED" if sync_success else "❌ SYNC FAILED"
                            print(f"{status} {name} ({d3e_type})")
                            new_loop.close()
                        except Exception as e:
                            print(f"❌ SYNC FAILED {name} - Error: {str(e)}")
                    
                    # Run in separate thread to avoid event loop conflicts
                    thread = threading.Thread(target=run_sync_in_thread)
                    thread.start()
                    thread.join(timeout=5)  # 5 second timeout
                    
                except Exception as e:
                    print(f"❌ SYNC FAILED {name} - Error: {str(e)}")
                    
        if components_found > 0:
            print(f"✅ Successfully processed {components_found} JSON components")
            return
            
    except json.JSONDecodeError:
        print("⚠️ Not valid JSON, trying legacy text parsing...")
        
    # Fallback to legacy text-based parsing
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
    processed = set()
    
    def extract_component_blocks_improved(text, component_type):
        blocks = []
        # Updated patterns to match correct D3E syntax
        patterns = [
            rf'\({component_type}\s+\w+\)\s*\{{',  # (Model Identity) {
            rf'\({component_type.lower()}\s+\w+\)\s*\{{',  # (model identity) {
            rf'{component_type}\s*\{{',  # Model {
            rf'{component_type}\s+\{{',  # Model {
            rf'{component_type.lower()}\s*\{{',  # model {
            rf'{component_type.lower()}\s+\{{',  # model {
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
            r"name\s*['\"]([^'\"]+)['\"]",  # name 'ComponentName'
            r"name\s*:\s*['\"]([^'\"]+)['\"]",  # name: 'ComponentName'
            r"name\s*=\s*['\"]([^'\"]+)['\"]",  # name = 'ComponentName'
            r"\((?:Model|Widget|Page|Style|Theme|OptionSet)\s+(\w+)\)",  # (Model Identity)
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
                    # Use asyncio.create_task instead of asyncio.run to avoid event loop conflict
                    import asyncio
                    import threading
                    
                    def run_sync_in_thread():
                        try:
                            new_loop = asyncio.new_event_loop()
                            asyncio.set_event_loop(new_loop)
                            sync_success, sync_message = new_loop.run_until_complete(update_code(ctx, d3e_type, name, block))
                            status = "✅ SYNCED" if sync_success else "❌ SYNC FAILED"
                            print(f"{status} {name} ({d3e_type})")
                            new_loop.close()
                        except Exception as e:
                            print(f"❌ SYNC FAILED {name} - Error: {str(e)}")
                    
                    # Run in separate thread to avoid event loop conflicts
                    thread = threading.Thread(target=run_sync_in_thread)
                    thread.start()
                    thread.join(timeout=5)  # 5 second timeout
                    
                except Exception as e:
                    print(f"❌ SYNC FAILED {name} - Error: {str(e)}")
                    
    if components_found == 0:
        print("⚠️ No D3E components found in AI output")