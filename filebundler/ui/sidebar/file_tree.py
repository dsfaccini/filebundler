# filebundler/ui/sidebar/file_tree.py
import logging
import streamlit as st

from filebundler.models.FileItem import FileItem
from filebundler.FileBundlerApp import FileBundlerApp

from filebundler.ui.sidebar.file_tree_buttons import render_file_tree_buttons

logger = logging.getLogger(__name__)


def render_file_tree(app: FileBundlerApp):
    """
    Render a file tree with checkboxes in the Streamlit UI

    Args:
        app: FileBundlerApp instance
    """

    st.subheader(
        f"Files ({app.selections.nr_of_selected_files}/{app.nr_of_files}) ({f'{app.selections.tokens}/{app.root_item.tokens}'} tokens)"
    )

    def clear_search():
        st.session_state["file_tree_search"] = ""

    # Add search bar
    search_col1, search_col2 = st.columns([1, 1])
    with search_col1:
        search_term = st.text_input("🔍 Search files", key="file_tree_search")
    with search_col2:
        if search_term:
            if st.button("Clear Search", on_click=clear_search):
                st.rerun()

    render_file_tree_buttons(app)

    highest_token_item = app.highest_token_item
    max_tokens = highest_token_item.tokens if highest_token_item else 0

    def get_token_color(tokens: int) -> str:
        """Get a color for a token count based on its value within the range."""
        min_tokens = 0
        if not tokens or tokens == 0 or max_tokens == min_tokens:
            return ""

        normalized = (tokens - min_tokens) / (max_tokens - min_tokens)
        if normalized < 0.1:
            return "✅"
        elif normalized < 0.3:
            return "⚠️"
        elif normalized < 0.5:
            return "❗"
        else:
            return "❗❗"

    def format_token_string(tokens: int) -> str:
        """Format the token count with a color."""
        if not tokens:  # Handles directories without a direct token count
            return ""
        color = get_token_color(tokens)
        if color:
            return f"""({tokens} tokens){color}"""
        return f"({tokens} tokens)"

    def matches_search(item: FileItem) -> bool:
        """Check if an item matches the search term"""
        if not search_term:
            return True
        search_lower = search_term.lower()
        return search_lower in item.name.lower()

    def has_matching_children(item: FileItem) -> bool:
        """Check if an item or any of its children match the search term"""
        if matches_search(item):
            return True
        return any(has_matching_children(child) for child in item.children)

    # Define recursive function to display directories and files
    def display_directory(file_item: FileItem, indent: int = 0):
        try:
            for child in file_item.children:
                # Skip if neither the item nor its children match the search
                if not has_matching_children(child):
                    continue

                token_str = format_token_string(child.tokens)
                indent_str = "&nbsp;" * indent * 4
                checkbox_label = (
                    f"{indent_str}->📁 **{child.name}** {token_str}"
                    if child.is_dir
                    else f"{indent_str}-> {child.name} {token_str}"
                )
                new_state = st.checkbox(
                    checkbox_label,
                    value=child.selected,
                    key=f"file_{child.path}", # TODO: handle symlinks
                    help=f"Select {child.name} for bundling",
                )

                # Handle checkbox change
                if new_state != child.selected:
                    child.toggle_selected()
                    app.selections.save_selections()
                    st.rerun()

                if child.is_dir:
                    display_directory(child, indent + 1)

        except Exception as e:
            logger.error(f"Error displaying directory: {e}", exc_info=True)
            st.error(f"Error displaying directory: {str(e)}")

    try:
        # Display the file tree starting from root
        if app.root_item:
            display_directory(app.root_item)
        else:
            st.info("Please wait for the file tree to be generated.")
    except Exception as e:
        logger.error(f"Error rendering file tree: {e}", exc_info=True)
        st.error(f"Error rendering file tree: {str(e)}")
