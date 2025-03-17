# Project Structure: file-bundler
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
├── 📁 .streamlit/
│   └── 📄 config.toml
├── 📁 filebundler/
│   ├── 📁 managers/
│   │   ├── 📄 BundleManager.py
│   │   ├── 📄 GlobalSettingsManager.py
│   │   ├── 📄 ProjectSettingsManager.py
│   │   └── 📄 SelectionsManager.py
│   ├── 📁 models/
│   │   ├── 📄 AppProtocol.py
│   │   ├── 📄 Bundle.py
│   │   ├── 📄 FileItem.py
│   │   ├── 📄 GlobalSettings.py
│   │   └── 📄 ProjectSettings.py
│   ├── 📁 services/
│   │   ├── 📄 code_export_service.py
│   │   └── 📄 project_structure.py
│   ├── 📁 ui/
│   │   ├── 📁 sidebar/
│   │   │   ├── 📄 file_tree.py
│   │   │   ├── 📄 project_selection.py
│   │   │   └── 📄 settings_panel.py
│   │   ├── 📁 tabs/
│   │   │   ├── 📄 export_contents.py
│   │   │   ├── 📄 global_settings_panel.py
│   │   │   ├── 📄 manage_bundles.py
│   │   │   └── 📄 selected_files.py
│   │   ├── 📄 confirm.py
│   │   └── 📄 notification.py
│   ├── 📁 utils/
│   │   ├── 📄 __init__.py
│   │   ├── 📄 filepath_checker.py
│   │   └── 📄 language_formatting.py
│   ├── 📄 constants.py
│   ├── 📄 FileBundlerApp.py
│   └── 📄 state.py
├── 📄 .env
├── 📄 .env.example
├── 📄 .gitignore
├── 📄 .python-version
├── 📄 main.py
├── 📄 mypy.ini
├── 📄 pyproject.toml
├── 📄 README.md
├── 📄 test-utils.ipynb
└── 📄 TODO.md
```
