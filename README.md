# FileBundler

```bash
uvx filebundler
```

## What is it?
File Bundler is a web app and CLI utility to bundle project files together and use them for LLM prompting. It helps estimate and optimize token and context usage.

# Who is FileBundler for?
If you're used to copying your files into your "chat of choice" and find the output is often better than the edits your AI powered IDE proposes then FileBundler is for you. 

**Here are some reasons why:**
1. Segment your projects into topics (manually or with AI)
2. Optimize your LLM context usage
3. Copy fresh context in one click, no uploading files, no "Select a file..." dialog
4. It encourages you to use best practices, like [anthropic's use of xml tags](https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/use-xml-tags)

# How do I use it?
- install and run FileBundler per the command at the start of this README
- visit the URL shown on your terminal
- you'll be prompted to enter the path of your project (this is your local filesystem path)
  - you can copy the path to your folder and paste it there
  - <details><summary>why no file selection window</summary>we currently don't support a "Select file" dialog but we're open to it if this is a major pain point</details>
- This will load the <span style="color:green">file tree 🌳</span> on the sidebar and the tabs on the right
- The tabs will display your currently selected files, allow you to save them in a bundle and export their contents to be pasted on your chat of preference
- To save a bundle you need to enter a name. The name must be lowercase and include only hyphens ("-") letters and numbers

# AI Features

## Auto-Bundle
TODO description -> what is it
TODO setup -> export ANTHROPIC_API_KEY='your-api-key'
TODO steps -> how do I use it

## Performance and debugging
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

# Similar tools

## Cursor
Currently, you can add project rules to your project and include globs for files related to those rules. This is kind of a reverse file bundler, since cursor uses the files in the glob to determine what rules you send to the LLM.
You can as well make a selection of files to be included in a chat, but you don't have an overview of how much context has been used. To clear the context you can start a new chat, but the selection you made for the previous chat won't be persisted (as of today), so you need to reselect your files.

## RepoPrompt
Before I started this tool I researched if there was already an existing tool and stumbled upon [Repo Prompt](https://x.com/RepoPrompt), which I believe is built by @pvncher. Some reasons I decided against using it were:
1. currently waitlisted
2. currently not available for Windows
3. closed source
4. pricing

For the record it seems like a great tool and I invite you to check it out. It offers lots of other functionality, like diffs and code trees.

## Result
Since I didn't find any other tool I decided to build FileBundler. 

Its main feature is bundling files together into reusable topics to prompt LLMs and review token usage. 

We currently use tiktoken with the [cl100k_base](https://github.com/openai/tiktoken) model to estimate token count, but you can may a utility like [tokencounter.org](https://tokencounter.org/) to estimate token usage for other models or [openai's tokenizer](https://platform.openai.com/tokenizer) to compare estimates.

# Useful references
- [anthropic's prompt library](https://docs.anthropic.com/en/prompt-library)
- [anthropic's long context tips](https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/long-context-tips#example-multi-document-structure)

# Roadmap
TODO.md