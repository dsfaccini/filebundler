---
description: Add Gemini LLM utility and provider abstraction to FileBundler
globs: ["filebundler/lib/llm/gemini.py", "filebundler/ui/tabs/auto_bundler/before_submit.py", "filebundler/lib/llm/auto_bundle.py", "filebundler/lib/llm/claude.py"]
alwaysApply: false
---
# Gemini LLM Utility & Provider Abstraction Implementation

Implements Gemini LLM support and abstracts provider/model selection in FileBundler. Updates the UI to allow users to select between Anthropic and Gemini, enter the correct API key, and caches the key in app state. Refactors LLM invocation logic to support multiple providers.

## Completed Subtasks

- [x] Create this task file
- [x] Create Gemini LLM utility in `filebundler/lib/llm/gemini.py`
- [x] Abstract provider/model selection in the auto-bundler UI
- [x] Update API key input and caching logic for multiple providers
- [x] Refactor LLM invocation to support multiple providers
- [x] Add logging and error handling for provider/model selection

## In Progress Subtasks

- [ ] Add unit tests for Gemini LLM utility in `filebundler/lib/llm/gemini.py`
- [ ] Add integration tests for provider/model selection logic in `filebundler/lib/llm/auto_bundle.py`
- [ ] Add UI tests for provider/model and API key selection in `filebundler/ui/tabs/auto_bundler/before_submit.py`
- [ ] Update documentation and README for Gemini support and provider abstraction

## Implementation Plan

1. Create a Gemini LLM utility module, mirroring the structure of the Claude utility.
2. Refactor the auto-bundler UI to allow provider selection and show the correct API key input.
3. Cache the API key for each provider in app state.
4. Update model selection to show models for the selected provider.
5. Refactor LLM invocation logic to call the correct provider utility.
6. Add robust logging and error handling for provider/model selection and API key issues.
7. Add tests and update documentation.

### Relevant Files

- filebundler/lib/llm/gemini.py - Gemini LLM utility
- filebundler/lib/llm/claude.py - Anthropic LLM utility (reference)
- filebundler/lib/llm/auto_bundle.py - LLM invocation logic
- filebundler/ui/tabs/auto_bundler/before_submit.py - UI for provider/model selection and API key input