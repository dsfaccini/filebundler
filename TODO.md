1. [QOL] modify the show_notification.. utility so it stacks notifications. currently, new notifications get displayed on top of not-yet vansihed notification. when two notifications get trigger at very near times, the older notification cannot be read.
   1. fix by stacking them! we can have an absolute container on the right side of the page and insert notification elements that vanish. new notifications start at the bottom, so the latest notifications get pushed to the top. 
2. [TEST] we haven't written any test
3. [PACKAGE] package as a library so people can install it and run it
   1. we need to add a license before packaging! apache 2.0 I guess?
   2. setup github actions AND SOMETHING TO MANAGE THE RELEASE VERSION!
      1. we'll start with 0.9
4. [DOCS] add pictures to README
5. [DOCS] make a video


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