# Project Path Validation and Platform Change Detection

Critical TODO implementation to handle project path changes and platform migrations by storing absolute paths in POSIX format and validating them on project load.

## Problem Statement

Currently, FileBundler doesn't store or validate the absolute project path in settings. When users:
- Move projects to different locations
- Switch between platforms (Windows ↔ macOS ↔ Linux) 
- Share project settings across different machines

The app may fail to work correctly because relative paths become invalid and bundle references break.

## Completed Subtasks

- [x] Analyzed current project path handling in codebase
- [x] Identified key files involved in project path management
- [x] Add absolute_project_path field to ProjectSettings model
- [x] Implement path validation logic in ProjectSettingsManager
- [x] Create UI for path update prompts
- [x] Add automatic path replacement functionality
- [x] Add comprehensive error handling for path validation failures


## Implementation Plan

### 1. Data Model Changes
- Add `absolute_project_path: Path` field to `ProjectSettings` model
- Store paths in POSIX format using `Path.as_posix()` for cross-platform compatibility
- Add validation that ensures the stored path matches the current project location

### 2. Path Validation Logic
- On project load, compare stored `absolute_project_path` with current `project_path`
- Detect platform changes by checking if path format has changed
- Implement automatic path replacement in all `.filebundler` directory files

### 3. User Interface Components
- Create warning dialogs for path mismatches
- Add update confirmation prompts
- Provide manual override options
- Show clear error messages when paths can't be resolved

### 4. File Update Mechanism
- Scan all JSON files in `.filebundler` directory for old path references
- Replace old paths with new paths in bundles, selections, and settings
- Maintain backup of original files during migration
- Validate all files after path replacement

### Architecture Flow

```
Project Load → Path Validation → Mismatch Detected → User Prompt → Auto-Update → Validation
```

### Key Validation Scenarios

1. **Project Moved**: Same platform, different directory
2. **Platform Change**: Windows ↔ macOS ↔ Linux with same relative structure  
3. **Complete Migration**: Different platform + different directory structure
4. **Shared Settings**: Project settings used across multiple machines

### Relevant Files

- `filebundler/models/ProjectSettings.py` - Add absolute_project_path field
- `filebundler/managers/ProjectSettingsManager.py` - Implement validation logic  
- `filebundler/ui/sidebar/project_selection.py` - Add user prompts and warnings
- `filebundler/FileBundlerApp.py` - Integrate path validation on initialization
- `filebundler/services/path_validation.py` - New service for path operations
- `filebundler/ui/components/path_migration_dialog.py` - New UI component for migration prompts

### Error Handling Strategy

- Graceful degradation when paths can't be resolved
- Clear user messaging about what went wrong
- Fallback to manual path entry
- Preserve user data integrity during migrations
- Comprehensive logging for debugging platform-specific issues

### Cross-Platform Considerations

- Use `pathlib.Path` for all path operations
- Store paths in POSIX format (`/` separators) regardless of platform
- Handle Windows drive letters and UNC paths appropriately
- Test path resolution on all major platforms
- Account for case sensitivity differences between filesystems