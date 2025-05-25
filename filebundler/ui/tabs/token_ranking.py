# filebundler/ui/tabs/token_ranking.py
import logging
import streamlit as st

from typing import List

from filebundler.models.FileItem import FileItem
from filebundler.FileBundlerApp import FileBundlerApp

logger = logging.getLogger(__name__)


def get_top_items_by_tokens(items: List[FileItem], count: int = 5) -> List[FileItem]:
    """
    Get the top N items sorted by token count in descending order.
    
    Args:
        items: List of FileItem objects
        count: Number of top items to return
        
    Returns:
        List of top items sorted by token count
    """
    # Filter out items with 0 tokens and sort by token count
    items_with_tokens = [item for item in items if item.tokens > 0]
    sorted_items = sorted(items_with_tokens, key=lambda x: x.tokens, reverse=True)
    return sorted_items[:count]


def render_token_ranking_list(items: List[FileItem], title: str, icon: str):
    """
    Render a list of items with their token counts.
    
    Args:
        items: List of FileItem objects to display
        title: Title for the section
        icon: Icon to display next to the title
    """
    st.subheader(f"{icon} {title}")
    
    if not items:
        st.info(f"No {title.lower()} found with tokens.")
        return
    
    for i, item in enumerate(items, 1):
        # Create a container for each item
        with st.container():
            col1, col2 = st.columns([3, 1])
            
            with col1:
                # Show rank number, relative path
                relative_path = item.relative
                st.write(f"**{i}.** `{relative_path}`")  # type: ignore
            
            with col2:
                # Show token count as a metric
                st.metric(
                    label="Tokens",
                    value=f"{item.tokens:,}",
                    delta=None
                )
            
            # Add a small divider except for the last item
            if i < len(items):
                st.divider()


def render_token_ranking_tab(app: FileBundlerApp):
    """
    Render the token ranking tab showing top folders and files by token count.
    
    Args:
        app: The FileBundlerApp instance
    """
    st.header("🏆 Token Ranking")
    st.write("Discover which folders and files consume the most tokens in your project.")  # type: ignore
    
    try:
        # Collect all folders and files
        folders = [fi for fi in app.file_items.values() if fi.is_dir and fi != app.root_item]
        files = [fi for fi in app.file_items.values() if not fi.is_dir]
        
        # Get top 5 folders and files by token count
        top_folders = get_top_items_by_tokens(folders, 5)
        top_files = get_top_items_by_tokens(files, 5)
        
        # Create two columns for side-by-side display
        col1, col2 = st.columns(2)
        
        with col1:
            render_token_ranking_list(top_folders, "Top 5 Folders", "📁")
        
        with col2:
            render_token_ranking_list(top_files, "Top 5 Files", "📄")
        
        # Add summary statistics
        st.divider()
        st.subheader("📊 Summary Statistics")
        
        summary_col1, summary_col2, summary_col3 = st.columns(3)
        
        with summary_col1:
            total_folders = len([f for f in folders if f.tokens > 0])
            st.metric("Folders with Tokens", total_folders)
        
        with summary_col2:
            total_files = len([f for f in files if f.tokens > 0])
            st.metric("Files with Tokens", total_files)
        
        with summary_col3:
            total_file_tokens = sum(f.tokens for f in files)
            st.metric("Total Tokens", f"{total_file_tokens:,}")
            
    except Exception as e:
        logger.error(f"Error rendering token ranking tab: {e}", exc_info=True)
        st.error(f"An error occurred while calculating token rankings: {str(e)}")
        st.write("Please ensure your project is properly loaded and files are accessible.")  # type: ignore