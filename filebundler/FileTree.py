# filebundler/file_tree.py
import logging
import streamlit as st

from pathlib import Path
from typing import Callable

logger = logging.getLogger(__name__)


def render_file_tree(
    file_items: dict,
    project_path: Path,
    selected_file_paths: set,
    toggle_file_selection: Callable,
):
    """
    Render a file tree with checkboxes in the Streamlit UI

    Args:
        file_items: Dictionary of FileItem objects
        project_path: Root path of the project
        selected_file_paths: Set of currently selected file paths
        toggle_file_selection: Callback function for toggling file selection
    """
    # Add custom CSS for scrollable tree
    st.markdown(
        """
    <style>
    /* Create scrollable container for files tree */
    [data-testid="stVerticalBlock"]:has(div.row-widget.stCheckbox) {
        max-height: 70vh;
        overflow-y: auto;
        padding-right: 10px;
    }
    </style>
    """,
        unsafe_allow_html=True,
    )

    # Subheader
    st.subheader("Files")

    # Define recursive function to display directories and files
    def display_directory(directory_item, indent=0):
        try:
            for child in directory_item.children:
                if child.is_dir:
                    # Directory entry
                    st.markdown(f"{'&nbsp;' * indent * 4}📁 **{child.name}**")
                    display_directory(child, indent + 1)
                else:
                    # File entry with checkbox
                    is_selected = child.path in selected_file_paths

                    # Using checkbox for selection
                    new_state = st.checkbox(
                        f"{'&nbsp;' * indent * 4} {child.name}",
                        value=is_selected,
                        key=f"file_{child.path}",
                        help=f"Select {child.name} for bundling",
                    )

                    # Handle checkbox change
                    if new_state != is_selected:
                        toggle_file_selection(child.path)
                        # Force refresh
                        st.rerun()
        except Exception as e:
            logger.error(f"Error displaying directory: {e}", exc_info=True)
            st.error(f"Error displaying directory: {str(e)}")

    try:
        # Display the file tree starting from root
        root_item = file_items[project_path]
        display_directory(root_item)
    except Exception as e:
        logger.error(f"Error rendering file tree: {e}", exc_info=True)
        st.error(f"Error rendering file tree: {str(e)}")
