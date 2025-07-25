
import requests
import json
import re

# Improved project selection logic (must come first)
from project_manager import list_projects, create_project
projects = list_projects()
if not projects:
    print("No projects found. Please enter a name for your new project:")
    while True:
        new_name = input("Project name: ").strip()
        if new_name:
            create_project(new_name)
            current_project = new_name
            break
        print("Project name cannot be empty.")
elif len(projects) == 1:
    current_project = projects[0]
    print(f"Automatically selected the only available project: {current_project}")
else:
    print("Available Projects:")
    for idx, proj in enumerate(projects, 1):
        print(f"  {idx}. {proj}")
    while True:
        choice = input(f"Select a project [1-{len(projects)}]: ").strip()
        if choice.isdigit():
            choice = int(choice)
            if 1 <= choice <= len(projects):
                current_project = projects[choice-1]
                break
        print("Invalid selection. Try again.")
print(f"\n📁 Using project: {current_project}")

# ✅ Context Manager Setup
import requests
import json
import re
import time
import asyncio
import threading
import os
from context_loader import ContextManager
from file_manager import create_or_update_file
from sync_manager import update_code, Context, start_file_watcher
from component_extractor import save_components_from_d3e_output
from project_manager import select_project
from config import CLAUDE_API_KEY, OPENAI_API_KEY, GEMINI_API_KEY, remote_config

# Improved project selection logic (must come first)
from project_manager import list_projects, create_project
projects = list_projects()
if not projects:
    print("No projects found. Please enter a name for your new project:")
    while True:
        new_name = input("Project name: ").strip()
        if new_name:
            create_project(new_name)
            current_project = new_name
            break
        print("Project name cannot be empty.")
elif len(projects) == 1:
    current_project = projects[0]
    print(f"Automatically selected the only available project: {current_project}")
else:
    print("Available Projects:")
    for idx, proj in enumerate(projects, 1):
        print(f"  {idx}. {proj}")
    while True:
        choice = input(f"Select a project [1-{len(projects)}]: ").strip()
        if choice.isdigit():
            choice = int(choice)
            if 1 <= choice <= len(projects):
                current_project = projects[choice-1]
                break
        print("Invalid selection. Try again.")
print(f"\n📁 Using project: {current_project}")

# ✅ Context Manager Setup
context_manager = ContextManager()

# Dynamic structure files to load
structure_files = []

# Load existing themes, styles, and models (after project selection)
def load_workspace_context():
    try:
        if 'current_project' in globals() and current_project:
            base_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'Projects', current_project)
            # Themes
            theme_dir = os.path.join(base_dir, 'StyleTheme')
            if os.path.exists(theme_dir):
                themes = os.listdir(theme_dir)
                print("✅ Loaded themes:", ", ".join([t.replace(".d3e", "") for t in themes if t.endswith(".d3e")]))
            # Styles
            style_dir = os.path.join(base_dir, 'Style')
            if os.path.exists(style_dir):
                styles = os.listdir(style_dir)
                print("✅ Loaded styles:", ", ".join([s.replace(".d3e", "") for s in styles if s.endswith(".d3e")]))
            # Models
            model_dir = os.path.join(base_dir, 'Model')
            if os.path.exists(model_dir):
                models = os.listdir(model_dir)
                print("✅ Loaded models:", ", ".join([m.replace(".json", "") for m in models if m.endswith(".json")]))
        else:
            print("⚠️ No project selected. Nothing loaded.")
    except Exception as e:
        print(f"⚠️ Error loading workspace context: {str(e)}")

context_manager.set_structure_files(structure_files)
load_workspace_context()
projects = list_projects()
if not projects:
    print("No projects found. Please enter a name for your new project:")
    while True:
        new_name = input("Project name: ").strip()
        if new_name:
            create_project(new_name)
            current_project = new_name
            break
        print("Project name cannot be empty.")
elif len(projects) == 1:
    current_project = projects[0]
    print(f"Automatically selected the only available project: {current_project}")
else:
    print("Available Projects:")
    for idx, proj in enumerate(projects, 1):
        print(f"  {idx}. {proj}")
    while True:
        choice = input(f"Select a project [1-{len(projects)}]: ").strip()
        if choice.isdigit():
            choice = int(choice)
            if 1 <= choice <= len(projects):
                current_project = projects[choice-1]
                break
        print("Invalid selection. Try again.")
print(f"\n📁 Using project: {current_project}")
context_manager.set_structure_files(structure_files)
load_workspace_context()

def build_system_message():
    ctx = context_manager.build_context()
    
    # Add theme information
    try:
        if 'current_project' in globals() and current_project:
            base_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'Projects', current_project)
            theme_dir = os.path.join(base_dir, 'StyleTheme')
            if os.path.exists(theme_dir):
                theme_files = [t for t in os.listdir(theme_dir) if t.endswith('.d3e')]
                if theme_files:
                    ctx["Available Themes"] = "\n".join([f"- {t.replace('.d3e', '')}" for t in theme_files])
            style_dir = os.path.join(base_dir, 'Style')
            if os.path.exists(style_dir):
                style_files = [s for s in os.listdir(style_dir) if s.endswith('.d3e')]
                if style_files:
                    ctx["Available Styles"] = "\n".join([f"- {s.replace('.d3e', '')}" for s in style_files])
    except Exception:
        pass

    context_str = "\n".join([f"=== {k} ===\n{v}" for k, v in ctx.items()])
    return f"""
You are a D3E Programming Language Expert. D3E is a standalone programming language like Dart, Java, or Python.
{context_str}
=== ENFORCEMENT ===
- ONLY generate D3E language code.
- NO HTML, CSS, JavaScript, or web framework code.
- D3E uses Widgets, Pages, Styles, Themes (Column, Row, TextView, etc.).
- ALWAYS reference existing themes and styles when creating widgets/pages.
- Use theme colors (@c1, @c2, etc.) instead of hardcoded colors.
- Reference existing styles where applicable (Primary, Secondary, Error, etc.).
- Consider any referenced models and their properties.
"""

def build_user_prompt(user_prompt):
    return f"""
Generate D3E programming language code for: {user_prompt}

IMPORTANT:
- Use only D3E syntax.
- No web or unrelated code.
"""

# ✅ Claude API
def call_claude(user_prompt):
    headers = {
        "x-api-key": CLAUDE_API_KEY,
        "anthropic-version": "2023-06-01",  # Required version for Claude 4
        "Content-Type": "application/json"
    }

    payload = {
        "model": "claude-opus-4-20250514",  # ✅ Latest Claude 4 model
        "max_tokens": 4096,
        "temperature": 0.7,
        "top_p": 0.95,
        "system": build_system_message(),
        "messages": [
            {"role": "user", "content": build_user_prompt(user_prompt)}
        ]
    }

    try:
        response = requests.post(
            "https://api.anthropic.com/v1/messages",
            headers=headers,
            json=payload,
            timeout=60
        )
        response.raise_for_status()
        data = response.json()

        # ✅ Claude 4 returns `content` as a list of text blocks
        return ''.join([part.get("text", "") for part in data.get("content", [])])

    except requests.exceptions.RequestException as e:
        print(f"❌ Claude API Error: {str(e)}")
        return None


# ✅ OpenAI API (ChatGPT)
def call_openai(user_prompt):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {OPENAI_API_KEY}"
    }
    payload = {
        "model": "gpt-4o-mini",
        "messages": [
            {"role": "system", "content": build_system_message()},
            {"role": "user", "content": build_user_prompt(user_prompt)}
        ]
    }
    r = requests.post("https://api.openai.com/v1/chat/completions", json=payload, headers=headers, timeout=30)
    r.raise_for_status()
    return r.json()["choices"][0]["message"]["content"]

# ✅ Gemini API
def call_gemini(user_prompt):
    headers = {"Content-Type": "application/json"}
    payload = {
        "contents": [{"parts": [{"text": build_user_prompt(user_prompt)}]}]
    }
    r = requests.post(
        f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={GEMINI_API_KEY}",
        json=payload,
        headers=headers,
        timeout=30
    )
    r.raise_for_status()
    return r.json()["candidates"][0]["content"]["parts"][0]["text"]

# ✅ Auto-Fallback
def call_with_fallback(user_prompt):
    providers = [
        ("Claude", call_claude),
        ("ChatGPT", call_openai),
        ("Gemini", call_gemini)
    ]
    for name, func in providers:
        try:
            print(f"🔄 Trying {name}...")
            return func(user_prompt)
        except Exception as e:
            print(f"⚠️ {name} failed: {e}")
    return "❌ All APIs failed."
# ✅ Utility: Multiline input
def multiline_input(prompt=""):
    print(prompt)
    lines = []
    while True:
        line = input()
        if line.strip() == "END":
            break
        lines.append(line)
    return "\n".join(lines)

# ✅ Start file watcher in background
watcher_thread = threading.Thread(target=lambda: start_file_watcher(project=current_project), daemon=True)
watcher_thread.start()

# ✅ Main Conversation Loop
while True:
    user_prompt = multiline_input("\n🧑 You (end with 'END' on a new line): ")
    if user_prompt.strip().lower() in ["exit", "quit"]:
        print("👋 Exiting D3E Language Assistant.")
        break



    # ✅ Handle special case: Dynamically set structure files based on user command
    if user_prompt.strip().lower().startswith("set structure "):
        # Example: set structure Documentation/Models/STRUCTURE.md
        path = user_prompt.strip()[len("set structure "):].strip()
        if path:
            structure_files.clear()
            structure_files.append(path)
            context_manager.set_structure_files(structure_files)
            print(f"✅ Set structure file: {path}")
        continue
    if user_prompt.strip().lower().startswith("add structure "):
        # Example: add structure Documentation/Widgets/STRUCTURE.md
        path = user_prompt.strip()[len("add structure "):].strip()
        if path and path not in structure_files:
            structure_files.append(path)
            context_manager.set_structure_files(structure_files)
            print(f"✅ Added structure file: {path}")
        continue


    # ✅ Check if prompt matches D3E file operations (Model/Page/etc.)
    component_patterns = {
        'model': r"(create|update) model (\w+):(.+)",
        'optionset': r"(create|update) optionset (\w+):(.+)",
        'widget': r"(create|update) widget (\w+):(.+)",
        'page': r"(create|update) page (\w+):(.+)",
        'style': r"(create|update) style (\w+):(.+)",
        'theme': r"(create|update) theme (\w+):(.+)"
    }
    component_type, component_match = None, None
    for c_type, pattern in component_patterns.items():
        match = re.match(pattern, user_prompt.strip(), re.IGNORECASE | re.DOTALL)
        if match:
            component_type = c_type
            component_match = match
            break


    if component_match:
        action = component_match.group(1).lower()
        component_name = component_match.group(2)
        component_content = component_match.group(3).strip()

        # For widgets and pages, ensure theme and style references (project-based)
        if component_type in ['widget', 'page']:
            try:
                has_theme = '@c' in component_content
                has_style = 'styles [' in component_content
                if not (has_theme and has_style):
                    print("⚠️ Adding theme and style references...")
                    if 'current_project' in globals() and current_project:
                        base_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'Projects', current_project)
                        theme_dir = os.path.join(base_dir, 'StyleTheme')
                        style_dir = os.path.join(base_dir, 'Style')
                        if not has_theme and os.path.exists(theme_dir):
                            theme_files = [t for t in os.listdir(theme_dir) if t.endswith('.d3e')]
                            if theme_files:
                                with open(os.path.join(theme_dir, theme_files[0]), encoding='utf-8') as f:
                                    theme_content = f.read()
                                    if '@c' in theme_content:
                                        print("ℹ️ Using theme colors from", theme_files[0])
                        if not has_style and os.path.exists(style_dir):
                            style_files = [s.replace('.d3e', '') for s in os.listdir(style_dir) if s.endswith('.d3e')]
                            if style_files:
                                print("ℹ️ Available styles:", ", ".join(style_files))
            except Exception as e:
                print(f"⚠️ Error checking theme/style context: {str(e)}")

        if create_or_update_file(component_type, component_name, component_content, project=current_project):
            d3e_type_map = {
                'model': 'Model',
                'optionset': 'OptionSet',
                'widget': 'Widget',
                'page': 'Page',
                'style': 'Style',
                'theme': 'StyleTheme'
            }
            ctx = Context(remote_config)
            try:
                sync_success, msg = asyncio.run(
                    update_code(ctx, d3e_type_map[component_type], component_name, component_content)
                )
                print(f"{'✅ SYNCED' if sync_success else '❌ SYNC FAILED'} {component_name} ({d3e_type_map[component_type]})")
            except Exception as e:
                print(f"❌ SYNC FAILED {component_name} - {e}")
        continue

    # ✅ Fallback: Use Multi-API LLM
    result = call_with_fallback(user_prompt)
    print(f"\n🤖 D3E Language AI:\n{result}")

    # ✅ Extract D3E Components & Save (project-aware)
    save_components_from_d3e_output(result, project=current_project)
