1. [ROADMAP] implement a general util for prompting llms using openrouter
   1. make the util so that we can dynamically choose the model
   2. use an enum to allow for model selection
   3. you can store this utility under filebundler/lib/llm/...
2. [ROADMAP] create a new tab after "Manage Bundles" called "Auto-Bundle"
   1. it has a chat where the user can write a prompt he wants to use on a different LLM to help him with his project
   2. our LLM checks the prompt and the file structure, as well as the available bundles (not the contents, only the bundle names and the files) and selects the files that it deems relevant to answer the prompt
   3. the "auto bundle" feature clears the current selection before selecting new files (add this as a warning in very visible text above the prompt area)
   4. the user can then review the selected files
3. [TEST] we haven't written any test
4. [PACKAGE] package as a library so people can install it and run it
   1. we need to add a license before packaging! apache 2.0 I guess?
   2. setup github actions AND SOMETHING TO MANAGE THE RELEASE VERSION!
      1. we'll start with 0.9
   3. BE SURE TO ALLOW THE USER TO DISABLE THE AUTO OPENING BROWSER when they run it
5. [DOCS] add pictures to README
6. [DOCS] make a video


# IGNORE FOR NOW (may become relevant later)
1. display file name in the file tree as they are
  1. at the moment, __init__.py file for example, are shown only as "init.py". Probably because the "__" is used by the markdown as formatting
2. we could provide a Dockerfile
3. [ROADMAP] improve token count: once we have the llm utility with open router we can add a button in the "exports" tab that calculates the amount of tokens in the export using the model that the user chooses
4. [FEATURE] allow the user to modify the order of the files in the bundle
   1. we can do this by adding an "index" value to the FileItem model
   2. but I'm not sure how to best implement the re-ordering in the UI 
   3. drag and drop would be great be appearently this is only possible with a (not very widely used) library
   4. we may be better off making a component ourselves