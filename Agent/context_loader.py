import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
README_PATH = os.path.join(BASE_DIR, 'README.md')
BASIC_WIDGET_PATH = os.path.join(BASE_DIR, 'Prompts/Widgets', 'basic-widget.md')
COMPLEX_INTERACTIVE_WIDGET_PATH = os.path.join(BASE_DIR, 'Prompts/Widgets', 'complex-interactive-widget.md')

def load_readme():
    with open(README_PATH, 'r', encoding='utf-8') as f:
        return f.read()

def load_basic_widget():
    with open(BASIC_WIDGET_PATH, 'r', encoding='utf-8') as f:
        return f.read()

def load_complex_interactive_widget():
    with open(COMPLEX_INTERACTIVE_WIDGET_PATH, 'r', encoding='utf-8') as f:
        return f.read() 