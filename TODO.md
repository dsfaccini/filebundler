1. [QOL] Refactor BundlerManager to persist bundles in a "bundles" subdirectory instead of the "bundles.json" file
   1.  bundles will be persisted to disk as ".filebundler/bundles/[bundle-name].json"
2. [ROADMAP] bundles should display the last date they were exported
   1. if the were never exported we don't need to display anything
   2. if the last exported date is earlier than the latest modification date of one of the files in the bundle we should color the displayed bundle orange and show a tooltip with a hover text like "files in this bundle have been modified after it was last exported: {last_modified_date = }
   3. lets create an model called "BundleMetadata" to store last_exported (e.g. bundle.metadata.export_stats.last_exported)
   4. add following stats as @property to the "Bundle" model 
      1. last_modified_date
      2. size (as the sum of the sizes of all files in the bundle)
      3. word_count: implement a utility function "compute_token_count" to count the words
3.  [PACKAGE] package as a library so people can install it and run it
   1. we need to add a license before packaging! apache 2.0 I guess?
   2. setup github actions AND SOMETHING TO MANAGE THE RELEASE VERSION!
      1. we'll start with 0.9
   3. BE SURE TO ALLOW THE USER TO DISABLE THE AUTO OPENING BROWSER when they run it
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
7. [FEATURE] add a searchbar above the filetree so we can filter by filename
8. [TEST] we haven't written any test
9. [DOCS] add pictures to README
10. [DOCS] make a video


# IGNORE FOR NOW (may become relevant later)
- display file name in the file tree as they are
  - at the moment, __init__.py file for example, are shown only as "init.py". Probably because the "__" is used by the markdown as formatting
- we could provide a Dockerfile