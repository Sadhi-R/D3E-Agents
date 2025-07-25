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

def create_or_update_file(component_type, name, content, project=None):
    """
    Save the file under the given project. If project is None, use global folders (legacy).
    """
    relative_dir = dir_mappings.get(component_type.lower())
    if not relative_dir:
        print(f"❌ Unknown component type: {component_type}")
        return False
    if project:
        component_dir = os.path.join(BASE_DIR, 'Projects', project, relative_dir)
    else:
        component_dir = os.path.join(BASE_DIR, relative_dir)
    component_file = os.path.join(component_dir, f"{name}.d3e")
    if not os.path.exists(component_dir):
        os.makedirs(component_dir)
        print(f"📁 Created {component_type} directory at {component_dir}")
    try:
        with open(component_file, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"✅ {component_type.capitalize()} '{name}' saved at {component_file}")
        return True
    except Exception as e:
        print(f"❌ Error saving {component_type} '{name}': {str(e)}")
        return False