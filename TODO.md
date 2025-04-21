1. [TEST] we haven't written any test
2. [QOL] any change we make now we need to change the readme to `uvx filebundler@latest` so the user uses the latest version
3. [DOCS] add pictures to README
4. [DOCS] make a video

# Big TODOs

## CLI entrypoint
allow the user to run `uvx filebundler cli [action]` in a project root to initialize the `FileBundlerApp` and perform an action without starting the streamlit server. For now the only action is `tree`, to generate the project's `.filebundler/project-structure.md` file. In the future we'll include other features, like `index` to index the codebase.
NOTE: to run the streamlit app the user must now run `uvx filebundler web [options]`

## Codebase indexing
**TODO**
1.  make a tab to index the codebase
   1. 