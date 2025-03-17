# FileBundler

```bash
# TODO
# install using uv
# run using uv
# uvx filebundler?
```

## What is it?
File Bundler is a web app and CLI utility to bundle project files together and use them for LLM prompting. It helps estimate and optimize token and context usage.

# How do I install it?
- Install FileBundler per the command above
- Run it

# Who is FileBundler for?
If you're used to copying your files into your "chat of choice" and find the output is often better than the edits your AI powered IDE proposes then FileBundler is for you. 
**Here are some reasons why:**
1. Segment your projects into topics
2. Optimize your LLM context usage
3. Copy fresh context in one click, no uploading files, no "Select a file..." dialog

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
Since I didn't find any other tool I decided to build FileBundler. Its main feature is bundling files together into reusable topics to prompt LLMs and review token usage. We currently use word count as a proxy for token usage. Computing token count directly on the app is a planned feature but not yet implemented. You can use a utility like [tokencounter.org](https://tokencounter.org/) for better estimates in the meantime!