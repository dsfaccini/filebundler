1. [ROADMAP] implement a general util for prompting llms using the pydantic-ai library
   1. make the util so that we can dynamically choose between claude haiku, sonnet 3.5 and sonnet 3.7
   2. use an enum to allow for model selection
   3. you can store this utility under filebundler/lib/llm/auto_bundle.py
   4. for now the utility only needs to send one message, later we will make a utility that allows for conversation and agent interaction
2. [ROADMAP] create a new tab after "Manage Bundles" called "Auto-Bundle" (filebundler/ui/tabs/auto_bundler.py)
   2. it has a text-area (chat) where the user can write a prompt he wants to use on an LLM to help him with his project and a submit button that sends the body to the LLM using out llm util from the last TODO
   3. when the user opens the tab, the application automatically generates the project structure and auto selects the file, it also auto-selects all bundle files
      1. we display a notification for 5 seconds so the user knows about this
   4. the currently selected files can be viewed in an expander with the title "Selected files {nr_of_selected_files}
   5. the user can deselect files
   7. when the user submits, we generate the export and append the the prompt. the body sent to the LLM finally has the following structure:
      1. the export  consists of the selected files, which in turn include the project structure file (freshly generated) and the available bundle files (not the contents of the bundles, only the bundle names and the files)
      2. the user prompt appended at the end
   8. we send a system prompt with the request: "You are a requirements engineer for the FileBundler app. FileBundler helps users to create bundles of files in their project that belong to certain topics. For example, all files that deal with payments can be added to a bundle called "payments". The user can use these bundles to develop their project by providing relevant context quickly to other assistants or colleagues. Your mission is to help the user select files in their project that provide relevant context fulfill the user's task. The user will provide you with information about their project, like the file structure of their project, bundles that they may already have created, and possibly files and their contents that they deem relevant to their task. You must answer in the JSON format that we provide you with. In this JSON format you may or may not include a message as advise to the user."
   9. the llm returns an object like {"name": "{some-bundle-name}", "files": {"very_likely_useful": ["file1", "dir2/file2"], "probably_useful": ["more-files"]}, "message": "the LLM can add a message e.g. "}
   10. the app automatically saves this bundle as "llm-auto-{rest-of-name}"
   11. finally lets include a field in our ProjectSetting model called "auto_bundle_settings" (make a model for this too)
       1.  the AutoBundleSettings has the fields "auto_refresh_project_structure" (bool=True) and "auto_include_bundle_files" (bool=True)
       2.  for backwards compatibility the ProjectSetting.auto_bundle_settings is optional and its default value is None
3. [TEST] we haven't written any test
4. [PACKAGE] package as a library so people can install it and run it
   1. we need to add a license before packaging! apache 2.0 I guess?
   2. setup github actions AND SOMETHING TO MANAGE THE RELEASE VERSION!
      1. we'll start with 0.9
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