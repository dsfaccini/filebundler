1. [QOL] we a bundle is activated we should populate the "Bundle Name" input field with the name of the activated bundle (so it's easy for the user to re-save it)
   1. we can set a field in the app
2. [BUG] deleted or renamed files are not removed from bundles
   1. we shoud fix this by checking that they exist when we load the bundle or we activate it
   2. we should display a notification so the user knows which files have changed and re-adds them to the bundle
3. [FEATURE] bundles should display the last date they were exported
   1. if the were never exported we don't need to display anything
   2. if the last exported date is earlier than the latest modification date of one of the files in the bundle we should color the displayed bundle yellow and show a tooltip that says "files in this bundle have been modified after it was last exported: {last_modified_date = }
   3. lets create an model called "BundleMetadata" to store last_exported (e.g. bundle.metadata.export_stats.last_exported)
   4. the last_modified_date can be a @property
   5. also the size of the bundle can be exposed as a @property (as the sum of the sizes of all files in the bundle)
   6. lastly we can add a word_count @property that uses a utility function "compute_token_count" to count the words
4. [ROADMAP] implement a general util for prompting llms using openrouter
   1. make the util so that we can dynamically choose the model
   2. use an enum to allow for model selection
   3. you can store this utility under filebundler/lib/llm/...
5. [ROADMAP] create a new tab after "Manage Bundles" called "Auto-Bundle"
   1. it has a chat where the user can write a prompt he wants to use on a different LLM to help him with his project
   2. our LLM checks the prompt and the file structure, as well as the available bundles (not the contents, only the bundle names and the files) and selects the files that it deems relevant to answer the prompt
   3. the "auto bundle" feature clears the current selection before selecting new files (add this as a warning in very visible text above the prompt area)
   4. the user can then review the selected files
6. [UX] notify about added pattern and empty the "add pattern" input after adding a pattern
7. [BUG] after adding a bundle, the bundle count is not updated on the "Bundle Manager" tab
   1. also after deleting a bundle this count is also not updated
8. [ROADMAP] move project selection and filetree to the sidebar
   1.  this way the user can hide the sidebar if the want to take a better look at the main content
   2.  we would need to implement tabs on the sidebar, so the user can switch between the project selection and file tree screens
9.  [ROADMAP] add tabs for project settings and global settings
    1.  this tabs should be on the main page
    2.  so the main page would have three tabs: FileBundler (where the selected files, exports and bundles are displayed), Project Settings and Global Settings


# IGNORE FOR NOW (may become relevant later)
- display file name in the file tree as they are
  - at the moment, __init__.py file for example, are shown only as "init.py". Probably because the "__" is used by the markdown as formatting
- add a scroll to the selected files list (it can get long and we may want to use the space underneath for something else)