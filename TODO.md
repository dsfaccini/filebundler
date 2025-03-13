1. [FEATURE] the user should know when the last export happens, as files may have changed since the last export
  1. also the files displayed should show their last modified date
      1. create @property fields on the Models to easily display file size and last modified datetime
2. [FEATURE] store and display word count and memory use for exported contents
  - propose the logic to compute this
  - this is a substitute for token count, so we don't worry about embeddings
3. [ROADMAP] implement a general util for prompting llms using openrouter
   1. make the util so that we can dynamically choose the model
   2. use an enum to allow for model selection
   3. you can store this utility under filebundler/lib/llm/...
4. [ROADMAP] create a new tab after "Manage Bundles" called "Auto-Bundle"
   1. it has a chat where the user can write a prompt he wants to use on a different LLM to help him with his project
   2. our LLM checks the prompt and the file structure, as well as the available bundles (not the contents, only the bundle names and the files) and selects the files that it deems relevant to answer the prompt
   3. the "auto bundle" feature clears the current selection before selecting new files (add this as a warning in very visible text above the prompt area)
   4. the user can then review the selected files
5. [UX] notify about added pattern and empty the "add pattern" input after adding a pattern
6. [BUG] update the displayed number of saved bundles after deleting one


# IGNORE FOR NOW (may become relevant later)
- display file name in the file tree as they are
  - at the moment, __init__.py file for example, are shown only as "init.py". Probably because the "__" is used by the markdown as formatting
- add a scroll to the selected files list (it can get long and we may want to use the space underneath for something else)