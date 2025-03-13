1. add a border to the file tree
2. the file tree already has all non-ignored files in the project. we should add an option to the file tree to export the current project structure to a file (.filebundler/project-structure.md)
3. we want to estimate token count when 1. selections are exported and 2. bundles are exported
  - so the token count is done whenever the user makes an export of contents
  - for saved bundles: the token count is persisted together with the bundle data, so it's displayed on load
  - the user needs to know when the last export happens, as files may have changed
  - also the file displayed should show their last modified date
  - lets implement a pydantic model for this, right now we are creating the dicts when we dump the json
    - pydantic can't validate Path types, so we need to add arbitrary types to model_config using ConfigDict
    - Path types also don'T serialize well, so we use a field_serializer to serialize them as posix
    - the pydantic class doesn't really need to validate any data, we just want to have the type to reduce complexity
      - that way file size and last modified datetime can be stored as properties and we can set up how they are displayed
- as for how to add token count, propose ways to estimate this
  - we could do it locally but I want to avoid heave dependencies, like having to download very large libraries or embbeding models locally on the user's computer
  - at the same time, if we want to use an API to produce the embbedings I'd like to put this under a subscription model
    - in that case we'd setup a default API pointing to our server that would provide the embbedings
    - the user should as well be able to change the base url to point to an API of their own!
    - TODO: propose 3 different ways we can implement this feature


# IGNORE FOR NOW (may become relevant later)
- add a scroll to the selected files list (it can get long and we may want to use the space underneath for something else)