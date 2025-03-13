1. [STYLE] add a border to the file tree
2. [QOL] add an "x" (remove) button next to each selected file, so they can be unselected from the preview
   1. this is so the user doesn't need to go look for the file in the file tree
3. [FEATURE] the file tree already has all non-ignored files in the project. we should add an option to the file tree to export the current project structure to a file (.filebundler/project-structure.md)
   1. the purpose of the file tree is too, so LLMs know about other files in the project that may not be included in a bundle
4. [FEATURE] the user should know when the last export happens, as files may have changed since the last export
  1. also the files displayed should show their last modified date
      1. create @property fields on the Models to easily display file size and last modified datetime
5. [FEATURE] store and display word count and memory use for exported contents
  - propose the logic to compute this
  - this is a substitute for token count, so we don't worry about embeddings
6. [ROADMAP] implement a general util for prompting llms using openrouter
   1. make the util so that we can dynamically choose the model
   2. use an enum to allow for model selection
   3. you can store this utility under filebundler/lib/llm/...
7. [ROADMAP] create a new tab after "Manage Bundles" called "Auto-Bundle"
   1. it has a chat where the user can write a prompt he wants to use on a different LLM to help him with his project
   2. our LLM checks the prompt and the file structure, as well as the available bundles (not the contents, only the bundle names and the files) and selects the files that it deems relevant to answer the prompt
   3. the "auto bundle" feature clears the current selection before selecting new files (add this as a warning in very visible text above the prompt area)
   4. the user can then review the selected files


# IGNORE FOR NOW (may become relevant later)
- display file name in the file tree as they are
  - at the moment, __init__.py file for example, are shown only as "init.py". Probably because the "__" is used by the markdown as formatting
- add a scroll to the selected files list (it can get long and we may want to use the space underneath for something else)