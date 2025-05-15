# An MCP server for filebundler

## What does it need to do

The first and only tool that the MCP server will offer will be that of exporting a bundle of files. That is, an LLM tells the MCP server what files to bundle, the filebundler MCP then bundles those files together and exports the code of those files using the [classic XML structure](../../README.md#bundles).

## What is the value in doing that?

AI coding IDEs offer the AI some tools like `read file`. These tool calls:
1. add to the overall duration of an AI interaction, as the AI needs to answer with the tool call, the IDE calls the tool and passes the result to the AI, which then answers. This is done for every single file read and is independent of the size of the file.
2. add to costs, since some IDEs have opted to charge per tool call.

Because of these reasons, having a tool that gets a list of filepaths and then provides the whole context in one call saves the user time and money.

## Implementation Details

The MCP server has been implemented as follows:

1.  **Server File**: A new file `filebundler/mcp_server.py` was created to house the MCP server logic.
2.  **MCP Framework**: The server uses `FastMCP` from the `mcp.server.fastmcp` module for quick setup.
3.  **Tool Definition**:
    *   A tool named `export_file_bundle` is registered with the MCP server.
    *   **Arguments**:
        *   `file_paths: List[str]`: A list of relative file paths (strings) to be included in the bundle.
        *   `project_path: str`: The absolute path to the root of the project.
        *   `bundle_name: str = "mcp-bundle"`: An optional name for the bundle (string), defaulting to "mcp-bundle".
    *   **Functionality**:
        *   It initializes `FileItem` objects for each valid file path provided, using the `project_path` for correct resolution.
        *   It creates a `Bundle` object using these `FileItem`s and the specified `bundle_name`.
        *   It calls the `export_code()` method on the `Bundle` object to generate an XML string containing the content of the bundled files.
        *   Error handling is included for invalid project paths or if no valid files are found.
    *   **Returns**: An XML string containing the bundled file contents, or an error message encapsulated in `<error>` tags.
4.  **Server Execution**:
    *   The `filebundler/mcp_server.py` file includes an `async def main()` function that initializes and runs the MCP server using `stdio_server`.
    *   It can be run directly using `python filebundler/mcp_server.py`.
5.  **CLI Integration**:
    *   The `filebundler/main.py` script (using `argparse`) has been updated to include a new subcommand: `mcp`.
    *   Running `python -m filebundler mcp` will start the MCP server.
    *   This subcommand imports and executes the `main()` function from `filebundler.mcp_server`.

The server listens for MCP messages over standard input/output (stdio).
