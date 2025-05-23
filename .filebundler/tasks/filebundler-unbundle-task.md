# Task: Implement FileBundler CLI Unbundle Feature

## Motivation
- Enable users to quickly recreate multiple files from a single code bundle (e.g. from LLM chats like ChatGPT, Claude, etc.)
- Avoid the need to copy/paste each file/artifact individually from chat outputs
- Support bundles formatted as XML, possibly wrapped in markdown code blocks

## Implementation Summary
- Added a new CLI command: `filebundler cli unbundle`
- Default flow: User copies the code bundle to clipboard, runs the command, and simply presses Enter (do NOT paste in the terminal)
- FileBundler fetches the bundle directly from the clipboard (using pyperclip)
- Fallback: If the user types any character and presses Enter, they can paste the bundle manually (visible), finishing with Ctrl+D (Unix/macOS) or Ctrl+Z then Enter (Windows)
- The script strips markdown code block markers (triple backticks) if present
- Parses the XML bundle, extracting each <document> with <source> (file path) and <document_content> (file content)
- Unescapes XML entities (e.g., &lt;, &gt;, &amp;) in file content
- Creates all files in the current directory, including subfolders as needed

## Key Design Decisions
- Clipboard-first approach for invisible, robust pasting (works in all terminals, avoids echo/overflow issues)
- Manual paste fallback for maximum flexibility
- Handles markdown code block wrapping and XML entity escaping automatically
- Provides clear error messages for short/invalid input or XML parse errors

## Limitations/Notes
- No cross-platform way to make multi-line manual paste invisible in all terminals; clipboard is the most robust solution
- Large pastes may still be limited by some terminals if using manual paste
- User must ensure the bundle is valid XML and includes all required tags

## Outcome
- Users can now create all files from a code bundle in one step, improving workflow with LLM chats and artifact-based code delivery
