import os

PROJECTS_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'Projects')

def list_projects():
    """Return a list of available project names."""
    if not os.path.exists(PROJECTS_DIR):
        return []
    return [d for d in os.listdir(PROJECTS_DIR) if os.path.isdir(os.path.join(PROJECTS_DIR, d))]

def select_project():
    """Select project - auto if one exists, prompt if multiple, create if none."""
    projects = list_projects()
    if not projects:
        new_name = input("No projects found. Enter new project name: ").strip()
        if new_name:
            create_project(new_name)
            return new_name
        return None
    elif len(projects) == 1:
        return projects[0]
    else:
        print("\nAvailable Projects:")
        for idx, proj in enumerate(projects, 1):
            print(f"  {idx}. {proj}")
        while True:
            choice = input(f"Select a project [1-{len(projects)}]: ").strip()
            if choice.isdigit():
                choice = int(choice)
                if 1 <= choice <= len(projects):
                    return projects[choice-1]
            print("Invalid selection. Try again.")

def create_project(name):
    """Create a new project directory structure if it doesn't exist."""
    proj_path = os.path.join(PROJECTS_DIR, name)
    if not os.path.exists(proj_path):
        os.makedirs(proj_path)
        for sub in ['Model', 'OptionSets', 'Widgets', 'Pages', 'Style', 'StyleTheme']:
            os.makedirs(os.path.join(proj_path, sub), exist_ok=True)
    return True

def cleanup_project(name):
    """Remove all files in a project (use with caution)."""
    proj_path = os.path.join(PROJECTS_DIR, name)
    if not os.path.exists(proj_path):
        print(f"Project '{name}' does not exist.")
        return
    for root, dirs, files in os.walk(proj_path):
        for file in files:
            os.remove(os.path.join(root, file))
    print(f"🧹 Cleaned up all files in project '{name}'.")
