---
description: 
globs: 
alwaysApply: false
---
# Task File Management Guide
<!-- https://github.com/elie222/inbox-zero/blob/main/.cursor/rules/task-list.mdc -->
Guidelines for creating and managing task lists in markdown files to track project progress

## Task File Creation

1. Create markdown task files under the `.filebundler/` folder:
   - Use a descriptive name relevant to the feature (e.g., `ASSISTANT_CHAT.md`)
   - Include a clear title and description of the feature being implemented

2. Structure the file with these sections:
   ```markdown
   # Feature Name Implementation
   
   Brief description of the feature and its purpose.
   
   ## Completed Subtasks
   
   - [x] Subtask 1 that has been completed
   - [x] Subtask 2 that has been completed
   
   ## In Progress Subtasks
   
   - [ ] Subtask 3 currently being worked on
   - [ ] Subtask 4 to be completed soon
   
   ## Future Subtasks
   
   - [ ] Subtask 5 planned for future implementation
   - [ ] Subtask 6 planned for future implementation
   
   ## Implementation Plan
   
   Detailed description of how the feature will be implemented.
   
   ### Relevant Files
   
   - path/to/file1.ts - Description of purpose
   - path/to/file2.ts - Description of purpose
   ```

## Task List Maintenance

1. Update the task list as you progress:
   - Mark subtasks as completed by changing `[ ]` to `[x]`
   - Add new subtasks as they are identified
   - Move subtasks between sections as appropriate

2. Keep "Relevant Files" section updated with:
   - File paths that have been created or modified
   - Brief descriptions of each file's purpose
   - Status indicators (e.g., ✅) for completed components

3. Add implementation details:
   - Architecture decisions
   - Data flow descriptions
   - Technical components needed
   - Environment configuration

## AI Instructions

When working with task files, the AI should:

1. Regularly update the task file after implementing significant components
2. Mark completed tasks with [x] when finished
3. Add new tasks discovered during implementation
4. Maintain the "Relevant Files" section with accurate file paths and descriptions
5. Document implementation details, especially for complex features
6. When implementing tasks one by one, first check which task to implement next
7. After implementing a task, update the file to reflect progress

## Example Task Update

When updating a task from "In Progress" to "Completed":

```markdown
## In Progress Tasks

- [ ] Implement database schema
- [ ] Create API endpoints for data access

## Completed Tasks

- [x] Set up project structure
- [x] Configure environment variables
```

Should become:

```markdown
## In Progress Tasks

- [ ] Create API endpoints for data access

## Completed Tasks

- [x] Set up project structure
- [x] Configure environment variables
- [x] Implement database schema
```