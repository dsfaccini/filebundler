# Project Structure: file-bundler
## Directory Structure
```
file-bundler/
├── 📁 .cursor/
│   └── 📁 rules/
│       ├── 📄 app-flow.md
│       ├── 📄 core-features.md
│       ├── 📄 general.md
│       ├── 📄 overview.md
│       ├── 📄 prd.md
│       └── 📄 testing.md
├── 📁 .filebundler/
│   ├── 📁 bundles/
│   │   ├── 📄 bundle-management.json
│   │   ├── 📄 bundles-and-exports.json
│   │   ├── 📄 testing-ui-and-state.json
│   │   └── 📄 testing-ui-and-state.txt
│   ├── 📄 project-structure.md
│   ├── 📄 selections.json
│   └── 📄 settings.json
├── 📁 .streamlit/
│   └── 📄 config.toml
├── 📁 docs/
│   ├── 📄 ci-cd.md
│   └── 📄 streamlit-testing-synthesized.md
├── 📁 filebundler/
│   ├── 📁 managers/
│   │   ├── 📄 BundleManager.py
│   │   ├── 📄 GlobalSettingsManager.py
│   │   ├── 📄 ProjectSettingsManager.py
│   │   └── 📄 SelectionsManager.py
│   ├── 📁 models/
│   │   ├── 📄 AppProtocol.py
│   │   ├── 📄 Bundle.py
│   │   ├── 📄 BundleMetadata.py
│   │   ├── 📄 FileItem.py
│   │   ├── 📄 GlobalSettings.py
│   │   └── 📄 ProjectSettings.py
│   ├── 📁 services/
│   │   ├── 📄 code_export_service.py
│   │   ├── 📄 project_structure.py
│   │   └── 📄 token_count.py
│   ├── 📁 ui/
│   │   ├── 📁 sidebar/
│   │   │   ├── 📄 file_tree.py
│   │   │   ├── 📄 file_tree_buttons.py
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
│   │   ├── 📄 language_formatting.py
│   │   └── 📄 project_utils.py
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
