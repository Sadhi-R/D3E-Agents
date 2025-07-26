# D3E-Agents Project Guide

## Project Overview
D3E-Agents is a Python-based project that manages and synchronizes D3E project components. It provides functionality for context management, file operations, and remote synchronization of D3E project files.

## Project Structure
```
├── Agent/                  # Core agent functionality
│   ├── agent.py           # Main agent implementation
│   ├── component_extractor.py
│   ├── config.py          # Configuration management
│   ├── context_manager.py # Project context handling
│   ├── file_manager.py    # File operations handler
│   └── sync_manager.py    # Remote synchronization
├── Documentation/         # Project documentation
├── GlobalTemplates/      # Template configurations
└── Projects/             # D3E projects directory
```

## Prerequisites
- Python 3.7 or higher
- Required Python packages (install via requirements.txt)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/Sadhi-R/D3E-Agents.git
cd D3E-Agents
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Configuration
1. Ensure your project configuration is set up in the appropriate project directory under `Projects/`
2. Configure remote sync settings in `Agent/remote_sync_config.json` if needed

## Running the Project

1. **Basic Usage**
   - Navigate to the project root directory
   - Run the main agent:
   ```bash
   python -m Agent.agent
   ```

2. **Project-Specific Operations**
   - The agent will automatically detect and manage .d3e files within project directories
   - File changes are monitored and synchronized automatically
   - Project context is maintained per project basis

## Key Features

1. **Context Management**
   - Automatic project context loading and management
   - Support for multiple project types

2. **File Operations**
   - Project-scoped file management
   - Handles .d3e file operations

3. **Remote Synchronization**
   - Automatic file watching and sync
   - Supports async operations with D3E server

## Project Components

### Models
- Basic models
- Abstract models
- Embedded models
- Transient models
- Singleton models

### Widgets
- Basic widgets
- Complex interactive widgets
- Widgets with data binding
- Widgets with event handlers
- Widgets with computed properties

### Documentation
Detailed documentation available in the `Documentation/` directory:
- Model Types
- Property Types
- Relationships
- Option Sets
- Widgets
- Pages
- Styles

## Troubleshooting

1. **Sync Issues**
   - Verify network connectivity
   - Check remote_sync_config.json settings
   - Ensure proper file permissions

2. **Context Loading Issues**
   - Verify project structure follows required format
   - Check file extensions (.d3e)
   - Validate project configuration files

## Support
For issues and feature requests, please create an issue in the GitHub repository.

## License
This project is proprietary and confidential. All rights reserved.
