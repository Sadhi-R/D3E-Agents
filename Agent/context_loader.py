import os

class ContextManager:
    """Manages loading context files (README, widget structures, etc.) for D3E generation."""
    def __init__(self, base_dir=None):
        self.base_dir = base_dir or os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.readme_path = os.path.join(self.base_dir, 'README.md')
        self.structure_files = []  # Additional structure files to load

    def set_structure_files(self, structure_files):
        """Set the list of additional structure/context files to include."""
        self.structure_files = structure_files

    def load_readme(self):
        with open(self.readme_path, 'r', encoding='utf-8') as f:
            return f.read()

    def load_structure_files(self):
        contents = {}
        for file_path in self.structure_files:
            abs_path = file_path if os.path.isabs(file_path) else os.path.join(self.base_dir, file_path)
            if os.path.exists(abs_path):
                with open(abs_path, 'r', encoding='utf-8') as f:
                    contents[os.path.basename(file_path)] = f.read()
        return contents

    def build_context(self):
        context = {'README': self.load_readme()}
        context.update(self.load_structure_files())
        return context