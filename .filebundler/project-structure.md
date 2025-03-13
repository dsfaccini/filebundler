# Project Structure: file-bundler
## Ignored Patterns
- `**/__pycache__/**`
- `.git/**`
- `.ruff_cache/**`
- `.venv/**`
- `node_modules/**`
- `uv.lock`
- `venv/**`

## Directory Structure
```
file-bundler/
├── 📁 .cursor/
│   └── 📁 rules/
│       └── 📄 prd.md
├── 📁 .filebundler/
│   ├── 📄 bundles.json
│   ├── 📄 project-structure.md
│   ├── 📄 selections.json
│   └── 📄 settings.json
├── 📁 filebundler/
│   ├── 📁 managers/
│   │   ├── 📄 BundleManager.py
│   │   ├── 📄 SelectionManager.py
│   │   └── 📄 SettingsManager.py
│   ├── 📁 models/
│   │   ├── 📄 Bundle.py
│   │   └── 📄 ProjectSettings.py
│   ├── 📁 ui/
│   │   ├── 📁 sidebar/
│   │   │   └── 📄 settings_panel.py
│   │   ├── 📁 tabs/
│   │   │   ├── 📄 export_contents.py
│   │   │   ├── 📄 manage_bundles.py
│   │   │   └── 📄 selected_files.py
│   │   ├── 📄 bundle_display.py
│   │   ├── 📄 confirm.py
│   │   ├── 📄 file_tree.py
│   │   ├── 📄 notification.py
│   │   └── 📄 project_selection.py
│   ├── 📁 utils/
│   │   ├── 📄 __init__.py
│   │   ├── 📄 filepath_checker.py
│   │   ├── 📄 language_formatting.py
│   │   └── 📄 project_structure.py
│   ├── 📄 constants.py
│   ├── 📄 FileBundlerApp.py
│   └── 📄 state.py
├── 📄 .gitignore
├── 📄 .python-version
├── 📄 main.py
├── 📄 pyproject.toml
├── 📄 README.md
└── 📄 TODO.md
```
