# Critical TODOs
1. In the settings file, set the absolute project path (as possix). When we load a new project we want to check that the platform hasn't changed or the project has been moved.
    - If it has changed we need to prompt the user to update the path. We can do this automatically by replacing the path in all files in the filebundler directory.
    - If the user decides against updating it we need to warn them to update it manually themselves, as the app will not work correctly.

# Big TODOs

## Add a gemini LLM utility
1. we need to update the input field where the user enters the anthropic key, it should read differently depending on what model provider the user chooses to use. Any API key entered needs to be cached in the app state

## MCP tools
1. project structure tool (`project-structure.md` isn't initialized if the user doesn't run the web ap or CLI) so the agent should be able to get it from the MCP server directly.

## Codebase indexing
**TODO**
1.  make a tab to index the codebase

## TESTING
1. [TEST] we haven't written any test

## MY TODOs
1. [DOCS] add more pictures to README
2. [DOCS] make a video
3. [TODO] remove logfire for now.