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
├── 📁 filebundler/
│   ├── 📁 managers/
│   │   ├── 📄 BundleManager.py
│   │   ├── 📄 SelectionsManager.py
│   │   └── 📄 SettingsManager.py
│   ├── 📁 models/
│   │   ├── 📄 Bundle.py
│   │   ├── 📄 FileItem.py
│   │   ├── 📄 GlobalSettings.py
│   │   └── 📄 ProjectSettings.py
│   ├── 📁 services/
│   │   └── 📄 project_structure.py
│   ├── 📁 ui/
│   │   ├── 📁 sidebar/
│   │   │   └── 📄 settings_panel.py
│   │   ├── 📁 tabs/
│   │   │   ├── 📁 manage_bundles/
│   │   │   │   ├── 📄 display_bundles.py
│   │   │   │   └── 📄 display_tab.py
│   │   │   ├── 📄 export_contents.py
│   │   │   └── 📄 selected_files.py
│   │   ├── 📄 confirm.py
│   │   ├── 📄 file_tree.py
│   │   ├── 📄 notification.py
│   │   └── 📄 project_selection.py
│   ├── 📁 utils/
│   │   ├── 📄 __init__.py
│   │   ├── 📄 filepath_checker.py
│   │   └── 📄 language_formatting.py
│   ├── 📄 constants.py
│   ├── 📄 FileBundlerApp.py
│   └── 📄 state.py
├── 📄 .gitignore
├── 📄 .python-version
├── 📄 main.py
├── 📄 pyproject.toml
├── 📄 README.md
├── 📄 test-utils.ipynb
└── 📄 TODO.md
```
