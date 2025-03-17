# filebundler/ui/file_tree.py
import logging
import streamlit as st

from filebundler.FileBundlerApp import FileBundlerApp
from filebundler.models.FileItem import FileItem
from filebundler.services.project_structure import (
    generate_project_structure,
    save_project_structure,
)
from filebundler.ui.notification import show_temp_notification

logger = logging.getLogger(__name__)


def render_file_tree(app: FileBundlerApp):
    """
    Render a file tree with checkboxes in the Streamlit UI

    Args:
        app: FileBundlerApp instance
    """
    # BUG this markdown is too wide, it also affects the File Selection tab
    # TODO apply a border only to the file tree
    st.markdown(
        """
    <style>
    /* Create scrollable container for files tree */
    [data-testid="stVerticalBlock"]:has(div.row-widget.stCheckbox) {
        max-height: 80vh;
        overflow-y: auto;
        padding-right: 10px;
    }
    </style>
    """,
        unsafe_allow_html=True,
    )

    st.subheader(f"Files ({app.nr_of_files})")

    col1, col2 = st.columns([1, 1])

    with col1:
        # this button has less text so it's smaller than the other ones
        # TODO make all buttons the same size
        if st.button("Select All", key="select_all", use_container_width=True):
            app.selections.select_all_files()
            st.rerun()

        if st.button(
            "Export Structure", key="export_structure", use_container_width=True
        ):
            try:
                # Generate project structure markdown
                structure_md = generate_project_structure(app)

                output_file = save_project_structure(app.project_path, structure_md)

                show_temp_notification(
                    f"Project structure exported to {output_file.relative_to(app.project_path)}",
                    type="success",
                )

                st.session_state.app.selections.selected_file = output_file

            except Exception as e:
                logger.error(f"Error exporting project structure: {e}", exc_info=True)
                show_temp_notification(
                    f"Error exporting project structure: {str(e)}", type="error"
                )

            st.rerun()

    with col2:
        if st.button("Unselect All", key="unselect_all", use_container_width=True):
            app.selections.clear_all_selections()
            st.rerun()

        if st.button(
            "Refresh Project", key="refresh_project", use_container_width=True
        ):
            if st.session_state.project_loaded:
                try:
                    st.session_state.app.refresh()  # this runs st.rerun for us
                    show_temp_notification("Project refreshed", type="success")
                except Exception as e:
                    logger.error(f"Error refreshing project: {e}", exc_info=True)
                    show_temp_notification(
                        f"Error refreshing project: {str(e)}", type="error"
                    )
            else:
                show_temp_notification("No project loaded", type="error")

    # Define recursive function to display directories and files
    def display_directory(file_item: FileItem, indent: int = 0):
        try:
            for child in file_item.children:
                checkbox_label = (
                    f"{'&nbsp;' * indent * 4}📁 **{child.name}**"
                    if child.is_dir
                    else f"{'&nbsp;' * indent * 4} {child.name}"
                )
                new_state = st.checkbox(
                    checkbox_label,
                    value=child.selected,
                    key=f"file_{child.path}",
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
        root_item = app.file_items[app.project_path]
        display_directory(root_item)
    except Exception as e:
        logger.error(f"Error rendering file tree: {e}", exc_info=True)
        st.error(f"Error rendering file tree: {str(e)}")
