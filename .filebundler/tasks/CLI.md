# CLI Entrypoint Implementation

Implement a CLI entrypoint so the user can run `uvx filebundler cli [action]` in a project root to initialize the `FileBundlerApp` and perform an action without starting the streamlit server. For now, the only action is `tree`, to generate the project's `.filebundler/project-structure.md` file. In the future, other actions like `index` will be added.

## Completed Subtasks

- [x] Create CLI task file and implementation plan
- [x] Add CLI subcommand parsing to main.py
- [x] Implement 'tree' action to generate project-structure.md
- [x] Add logging and error handling for CLI actions
- [x] Update pyproject.toml if needed for CLI entrypoint
- [x] Centralize CLI logic for project structure in cli_entrypoint function
- [x] Add documentation for CLI usage in README

## In Progress Subtasks

- [ ] Generate tests for CLI actions

## Future Subtasks

- [ ] Implement 'index' and other future CLI actions
- [ ] Add tests for CLI actions

## Implementation Plan

- Refactor `main.py` to support subcommands: `web` (default, launches Streamlit) and `cli` (runs CLI actions)
- For `uvx filebundler cli tree`, call the centralized `cli_entrypoint` in `filebundler/services/project_structure.py` to avoid boilerplate
- Use argparse for subcommand parsing
- Add robust logging and error handling for CLI actions
- Ensure CLI does not start Streamlit server for CLI actions
- Document CLI usage in README

### Relevant Files

- filebundler/main.py - Main entrypoint, now calls cli_entrypoint for CLI actions
- filebundler/services/project_structure.py - Contains cli_entrypoint and logic to generate and save project structure
- pyproject.toml - Entry point for CLI
- README.md - Add CLI usage documentation