# FileBundler

## Running with uvx
You can run filebundler with uvx without installing it
```bash
uvx filebundler #  -> prints the version
uvx filebundler web [options] #  -> launches the web app
uvx filebundler web --headless #  -> no auto open
uvx filebundler web --theme #  -> light|dark
uvx filebundler web --log-level debug #  or one of [debug|info|warning|error|critical]
uvx filebundler cli tree [project_path] #  -> generates .filebundler/project-structure.md for the given project (default: current directory)
uvx filebundler cli chat_instructions
uvx filebundler cli unbundle # -> run these two together to paste multiple files from a chatbot into your project in a single move
uvx filebundler mcp # -> starts the MCP server
```

## Installing as a uv tool (Recommended)
```bash
uv tool install filebundler@latest

# after installing filebundler as a uv tool you can run it as a global command like:
# filebundler web
# filebundler cli
# without reinstalling the package each time (that is, downloading all dependencies each time)

# WARNING: If you already installed FileBundler as a local MCP server, close any process using the MCP server before uninstalling or upgrading FileBundler, as you may get a permission's error.
# uv tool uninstall filebundler
# uv tool upgrade filebundler
```

## What is it?
FileBundler is an MCP server, web app, and CLI utility to bundle project files together and use them for LLM prompting. It helps estimate and optimize token and context usage.

# Why use FileBundler?
```
Can I throw this whole folder into the chat?
How many tokens do I need for this feature?
The agent has spend 3 minutes listing directories and reading files
```
By creating file bundles you keep an overview of what parts of your codebase work with each other. You can optimize context usage by keeping track of how many tokens a certain area of your codebase takes.

Using the MCP server to bundle files together can save you time and money while your agent gathers context. [Here's an explanation why](./.filebundler/tasks/filebundler-MCP-server.md#what-is-the-value-in-doing-that)

**More reasons why you would want to use FileBundler:**
1. Segment your projects into topics (manually or with AI)
2. Optimize your LLM context usage
3. Copy fresh context in one click, no uploading files, no "Select a file..." dialog
4. It encourages you to use best practices, like [anthropic's use of xml tags](https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/use-xml-tags)

# How to use the Web App?
- Install and run FileBundler per the command at the start of this README
-
- visit the URL shown on your terminal
- you'll be prompted to enter the path of your project (this is your local filesystem path)
  - you can copy the path to your folder and paste it there
  - <details><summary>why no file selection window</summary>we currently don't support a "Select file" dialog but we're open to it if this is a major pain point</details>
- This will load the <span style="color:green">file tree 🌳</span> on the sidebar and the tabs on the right
- The tabs will display your currently selected files, allow you to save them in a bundle and export their contents to be pasted on your chat of preference
- To save a bundle you need to enter a name. The name must be lowercase and include only hyphens ("-") letters and numbers

# Features
Besides creating bundles FileBundler has additional features

## Project Structure
The app automatically exports your project structure to a file called `project-structure.md` with computed token counts for each file and folder not ignored. Checkout the [.filebundler/project-structure.md](https://raw.githubusercontent.com/dsfaccini/filebundler/refs/heads/master/.filebundler/project-structure.md) file in this project

## Ignore patterns
Not all files are included in the `project-structure.md`. *Ignore patterns* are made from a combination of `DEFAULT_IGNORE_PATTERNS` defined in this project and the .gitignore file of the project you open.

Ignore patterns are stored in the `.filebundler/settings.json` file can be modified either directly in this file or using the *webapp* in the `Project Settings` tab on the sidebar you can add or remove glob patterns to ignore certain files or folders from the project structure.

## Estimate token usage
We currently use tiktoken with the [o200k_base](https://github.com/openai/tiktoken) model to compute token count, but you may a utility like [tokencounter.org](https://tokencounter.org/) to estimate token usage for other models or [openai's tokenizer](https://platform.openai.com/tokenizer) to compare estimates.

## Bundles
A bundle is just a list of file paths relative to their project folder. It includes some metadata, such as the total byte size of the files in the bundle and the total tokens as calculated by our tokenizer (currretly o200k_base). A bundle can be exported, that means, the contents of the files listed in a bundle can be exported as an XML structure. This follows the best practices [mentioned above](#who-is-filebundler-for). This exported code is also called a bundle. So for clarity, we'll speak of "XML bundle" or "code bundle" when we talk about the **bundle of exported code** and refer to the list of file paths as the "file bundle" or just "bundle".

### Unbundle
Copy multiple files written by a chatbot using the CLI `unbundle` command.
```bash
filebundler cli chat_instructions # this copies the instrction to your clipboard, paste this instruction in your chat so the chatbot formats their response properly.
filebundler cli unbundle # this gives you a moment to copy the XML response from the chatbot into your clipboard.

# you don't need to paste the content into the terminal, just press enter when you're ready
# unbundle will unbundle the contents of your clipboard into the files and folders defined by the llm using their relative paths

# NOTE we suggest you do this after committing your staged files so you can more clearly see what changes were done
# Second note: if the format isn't right the function will fail
```

### Persistance
Bundles are also persisted to the project whenever they are created using the web app. They are JSON files found under `.filebundler/bundles`. You can also create a bundle by writing such a JSON file in the bundles folder.

## Auto-Bundle
The auto-bundler uses an LLM to suggest you bundles relevant to your query. Simply choose your desired model from the "Select LLM model" dropdown; the app will automatically infer the correct provider (Anthropic or Gemini) and prompt you for the corresponding API key if needed. The auto-bundler automatically selects your exported project structure (which you can unselect if you want).

The auto-bundler will use your prompt and current selections to suggest bundles. The LLM will return a list of likely and probable files that are relevant to your query, and a message and/or code if you asked for it.

### Auto-Bundle example
A workflow example would be for you to provide the LLM with your TODO list (TODO.md) and ask it to provide you with the files that are related to the first n tasks. You could also ask it to sort your tasks into different categories and then re-prompt it to provide bundles for each category.

## Tasks
FileBundler will copy the templates under [tasks/templates/](https://github.com/dsfaccini/filebundler/tree/master/filebundler/features/tasks/templates) into the project's `.filebundler/tasks/` directory when filebundler is initialized. This is a useful task management workflow. This will have no effect as long as your AI coding agent doesn't read the file. To use the task management workflow, you need to tell your agent to follow the instructions of the task management workflow using a trigger word or phrase, like `use the task management system whenever I tell you to "tackle a task"`.

## MCP
FileBundler includes a Model Context Protocol (MCP) server that allows AI-powered IDEs and other tools to programmatically request file bundles. This enables an LLM to receive the content of multiple specified files in a single, efficient transaction, potentially reducing interaction time and costs associated with multiple individual file-reading tool calls.

The server provides a tool named `export_file_bundle` which accepts a list of relative file paths, the absolute project path, and an optional bundle name. It returns an XML-formatted string containing the content of these files, ready for LLM consumption.

### Add the MCP server via JSON (like on Cursor)
If you want to use uvx, this is the JSON to install the MCP server
```json
{
    "mcpServers": {
      "filebundler-server": {
        "command": "uvx",
        "args": ["filebundler", "mcp"],
        "description": "Bundles a the contents of a list of files together into a single XML file"
      }
    }
  }
```

If you install filebundler as a tool, the `command` and `args` fields need to look like this:
```json
{
  // ...
  "command": "filebundler",
  "args": ["mcp"],
  // ...
}
```

Once configured, the AI in your IDE should be able to call the `export_file_bundle` tool, providing it with a list of file paths (these can be relative to the project root) and the absolute `project_path` of the project root to get a bundled context.

### Prime your agent to use the filebundler MCP
Example:
```
look at this task @filebundler-MCP-server.md . Check the @project-structure.md to get a list of the files you want to read in order to tackle this task. Instead of reading the files one by one, make a list of the files you think you need and use the filebundler mcp server to get a bundle of them. Use proper filesystem notation for the project path in the current operating system (i.e. C:\\path\\to\\project for Windows and /path/to/project for linux)
```

## CLI Usage
FileBundler supports a CLI mode for project actions without starting the web server.

### Export the project structure
To generate the project structure markdown file for your project, run:

```bash
filebundler cli tree [project_path]
```
- `project_path` is optional; if omitted, the current directory is used.
- The output will be saved to `.filebundler/project-structure.md` in your project.

### Paste multiple code files from a chatbot into your project
To quickly create files from a code bundle (e.g. from an LLM chat), run:

```bash
filebundler cli chat_instructions && filebundler cli unbundle
# chat_instructions copies the instructions you need to give your chat to format the output files in xml
# unbundle will unbundle the contents of your clipboard after you have copied the response from your chat
# NOTE "unbundle" assumes your LLM has followed the instructions and formatted your code in the described xml format
# if the format isn't right the function will fail
```
- **Recommended:** Copy the code bundle to your clipboard, then simply press Enter when prompted (do NOT paste in the terminal; FileBundler will fetch it directly from your clipboard).

### Print version
If you run `filebundler` with no subcommand, it prints the current version of the package.
You can also explicitly run `filebundler -v`

## Supported LLM models
The auto-bundler supports models from multiple providers (Anthropic and Gemini). Simply choose any supported model from the "Select LLM model" dropdown; the app will infer its provider and prompt for the matching API key (e.g. `ANTHROPIC_API_KEY` or `GEMINI_API_KEY`). To add more models or providers, extend the `MODEL_REGISTRY` in `filebundler/lib/llm/registry.py`.

# Roadmap
[TODO.md](https://raw.githubusercontent.com/dsfaccini/filebundler/refs/heads/master/TODO.md)
We plan on adding other features, like more MCP tools and codebase indexing.

# Performance and debugging
If your application **doesn't start or freezes** you can check the logs in your terminal.

If your application **hangs** on certain actions, you can debug using logfire. For this you'll need to stop FileBundler, set your logfire token and re-run the app.

You can set your logfire token like this
<details>
<summary>Unix/macOS</summary>

```bash
export LOGFIRE_TOKEN=your_token_here
```
</details>

<details>
<summary>Windows</summary>

```powershell
# using cmd
set LOGFIRE_TOKEN=your_token_here

# or in PowerShell
$env:LOGFIRE_TOKEN = "your_token_here"
```
</details>

For any other issues you may open an issue in the [filebundler repo](https://github.com/dsfaccini/filebundler).

## Errors

### Access or permission denied
Beware that if you install FileBundler as an MCP server for your IDE (e.g. Cursor, Windsurf, etc) or coding agent, that you may get permission's errors when upgrading or uninstalling FileBundler, if your coding agent is currently running.
```
error: failed to remove directory `C:\Users\user\AppData\Roaming\uv\tools\filebundler`: Access is denied. (os error 5)
```
### Wrong path syntax
Sometimes a model will use the wrong syntax for the project path, like this:
`/c:/Users/david/projects/filebundler`
Even though the tool call will fail, the error message helps the agent auto-correct and call the tool again with the proper syntax.

# Similar tools

## [Cursor](https://www.cursor.com/)
Currently, you can add project rules to your project and include globs for files related to those rules. This is kind of a reverse file bundler, since cursor uses the files in the glob to determine what rules you send to the LLM.
You can as well make a selection of files to be included in a chat, but you don't have an overview of how much context has been used. To clear the context you can start a new chat, but the selection you made for the previous chat won't be persisted (as of today), so you need to reselect your files.

## RepoPrompt
Before I started this tool I researched if there was already an existing tool and stumbled upon [Repo Prompt](https://x.com/RepoPrompt), which I believe is built by @pvncher. Some reasons I decided against using it were:
1. currently waitlisted
2. currently not available for Windows
3. closed source
4. pricing
5. ~~Can't create bundles or persist file selections~~ I believe this has been added since around April 2025.

It seems like a great tool and I invite you to check it out. It offers lots of other functionality, like diffs and code trees.

## [Claude Code](https://docs.anthropic.com/en/docs/agents-and-tools/claude-code/overview)
Like cursor but on the CLI. With the introduction of [commands](https://x.com/_catwu/status/1900593730538864643) you can save markdown files with your prompts and issue them as commands to claude code. This is a bit different than bundling project files into topics, but shares the concept of persisting workflows that you repeat as settings.

## aider
TODO

# Useful references
- [anthropic's prompt library](https://docs.anthropic.com/en/prompt-library)
- [anthropic's long context tips](https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/long-context-tips#example-multi-document-structure)

# LICENSE
We use GPLv3. Read it [here](https://raw.githubusercontent.com/dsfaccini/filebundler/refs/heads/master/LICENSE)

# UI
![Tab for exporting the code bundle](./docs/images/export-code-tab.png)

# Examples
[How does a code bundle look like?](./docs/example-bundle.xml)

# Running locally
```bash
# git clone .../dsfaccini/filebundler.git
# cd filebundler
streamlit run filebundler/main.py --global.developmentMode=false
```
