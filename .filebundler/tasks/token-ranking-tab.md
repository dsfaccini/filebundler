# Token Ranking Tab Implementation

Implements a new tab called "Token Ranking" that displays the top 5 folders and top 5 files with the highest number of tokens in two columns. This provides users with insights into which parts of their project consume the most tokens.

## Completed Subtasks

- [x] Analyze existing app structure and token counting logic
- [x] Understand UI tab pattern and FileItem token property
- [x] Create task file following project guidelines
- [x] Create token ranking tab UI component
- [x] Implement folder token ranking logic
- [x] Implement file token ranking logic
- [x] Add token ranking tab to main app navigation

## In Progress Subtasks


## Future Subtasks

- [ ] Add filtering capabilities
- [ ] Add export functionality for rankings
- [ ] Add visual token usage charts

## Implementation Plan

The token ranking tab will leverage the existing token counting infrastructure:

1. **Token Data Source**: Use the existing `FileItem.tokens` property which:
   - For files: calculates tokens using `count_tokens()` from `token_count.py`
   - For folders: sums tokens from all children recursively

2. **UI Structure**: Create a new tab component following the existing pattern:
   - Two column layout (folders on left, files on right)
   - Display top 5 items in each category
   - Show token count and relative path for each item

3. **Ranking Logic**: 
   - Collect all folders and files from the app's file tree
   - Sort by token count in descending order
   - Take top 5 from each category

4. **Integration**: Add the new tab to the main app navigation alongside existing tabs

### Relevant Files

- filebundler/ui/tabs/token_ranking.py - New tab component for token ranking ✅ (to be created)
- filebundler/app.py - Main app file to add new tab to navigation ✅ (to be modified)
- filebundler/models/FileItem.py - Existing model with token calculation logic ✅ (reviewed)
- filebundler/services/token_count.py - Existing token counting service ✅ (reviewed)

### Technical Implementation Details

- **Data Collection**: Traverse the app's file tree to collect all FileItem objects
- **Filtering**: Separate folders (directories) from files
- **Sorting**: Sort each category by token count (descending)
- **Display**: Use Streamlit columns and metrics for clean presentation
- **Performance**: Consider caching for large projects if needed