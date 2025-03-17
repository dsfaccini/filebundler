1. [QOL] Refactor BundlerManager to persist bundles in a "bundles" subdirectory instead of the "bundles.json" file
   1. bundles will be persisted to disk as ".filebundler/bundles/[bundle-name].json"
2. [BUG] The Global Settings tab is shown properly before a porject is loaded, but the content of the tab disappears once we open a project. Find the reason and fix it.
3. [ROADMAP] bundles should display the last date they were exported
   1. if the were never exported we don't need to display anything
   2. if the last exported date is earlier than the latest modification date of one of the files in the bundle we should color the displayed bundle orange and show a tooltip with a hover text like "files in this bundle have been modified after it was last exported: {last_modified_date = }
   3. lets create an model called "BundleMetadata" to store last_exported (e.g. bundle.metadata.export_stats.last_exported)
   4. add following stats as @property to the "Bundle" model 
      1. last_modified_date
      2. size (as the sum of the sizes of all files in the bundle)
      3. word_count: implement a utility function "compute_token_count" to count the words
4. [ROADMAP] implement a general util for prompting llms using openrouter
   1. make the util so that we can dynamically choose the model
   2. use an enum to allow for model selection
   3. you can store this utility under filebundler/lib/llm/...
5. [ROADMAP] once we have this llm utility with open router we can add a button in the "exports" tab that calculates the amount of tokens in the export using the model that the user chooses
6. [ROADMAP] create a new tab after "Manage Bundles" called "Auto-Bundle"
   1. it has a chat where the user can write a prompt he wants to use on a different LLM to help him with his project
   2. our LLM checks the prompt and the file structure, as well as the available bundles (not the contents, only the bundle names and the files) and selects the files that it deems relevant to answer the prompt
   3. the "auto bundle" feature clears the current selection before selecting new files (add this as a warning in very visible text above the prompt area)
   4. the user can then review the selected files
7.  [ROADMAP] add a tab for global settings
    1.  this tab should be on the main page
    2.  so the main page would have three tabs: "FileBundler", "About" and "Global Settings"
8.  [TEST] we haven't written any test


# IGNORE FOR NOW (may become relevant later)
- display file name in the file tree as they are
  - at the moment, __init__.py file for example, are shown only as "init.py". Probably because the "__" is used by the markdown as formatting
- add a scroll to the selected files list (it can get long and we may want to use the space underneath for something else)