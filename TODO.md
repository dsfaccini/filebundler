1. add a border to the file tree
2. add an "x" (remove) button next to each selected file, so they can be unselected from the preview
   1. this is so the user doesn't need to go look for the file in the file tree
3. the file tree already has all non-ignored files in the project. we should add an option to the file tree to export the current project structure to a file (.filebundler/project-structure.md)
   1. the purpose of the file tree is too, so LLMs know about other files in the project that may not be included in a bundle
4. the user should know when the last export happens, as files may have changed since the last export
  - also the files displayed should show their last modified date
  - right now we are creating the dictionaries for the bundle when we dump the json
    - lets implement a pydantic model the bundles
    - the pydantic class doesn't really need to validate any data, we just want to have the static type checks
    - REMBEMBER TO USE PYDANTIC V2 SYNTAX
    - add field_serializers for Path types, serialize them as posix
      - create @propertys to store file size and last modified datetime
5. store and display word count and memory use for exported contents
  - propose the logic to compute this
  - this is a substitute for token count, so we don't worry about embeddings


# IGNORE FOR NOW (may become relevant later)
- display file name in the file tree as they are
  - at the moment, __init__.py file for example, are shown only as "init.py". Probably because the "__" is used by the markdown as formatting
- add a scroll to the selected files list (it can get long and we may want to use the space underneath for something else)