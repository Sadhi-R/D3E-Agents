import os

dir_mappings = {
    'model': 'Model',
    'optionset': 'optionSets',
    'widget': 'Widgets',
    'page': 'Pages',
    'style': 'Style',
    'theme': 'StyleTheme',
    'styletheme': 'StyleTheme',
}

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def create_or_update_file(component_type, name, content, project):
    """
    Save or update the file only inside an existing project and correct subfolder.
    No global or outside creation/updation. Project must be provided and already exist.
    """
    relative_dir = dir_mappings[component_type.lower()]
    component_dir = os.path.join(BASE_DIR, 'Projects', project, relative_dir)
    if not os.path.exists(component_dir):
        os.makedirs(component_dir)
    component_file = os.path.join(component_dir, f"{name}.d3e")
    try:
        with open(component_file, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    except Exception:
        return False