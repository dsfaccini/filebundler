# filebundler/ui/tabs/selected_files.py
import logging
import streamlit as st

from pathlib import Path

from filebundler.FileBundlerApp import FileBundlerApp
from filebundler.ui.notification import show_temp_notification
from filebundler.utils.language_formatting import set_language_from_filename

logger = logging.getLogger(__name__)


def render_selected_files_tab(app: FileBundlerApp):
    """Render the Selected Files tab"""
    st.subheader(f"Selected Files ({app.selections.nr_of_selected_files})")
    st.text(
        "Click on a file to view its content. Click 'x' to remove a file from selection."
    )

    # TODO make this section scrollable, set a max height
    if app.selections.selected_file_items:
        for file_item in app.selections.selected_file_items:
            if file_item.is_dir:
                continue

            relative_path = file_item.path.relative_to(app.project_path)

            # Create a row with file button and remove button
            col1, col2 = st.columns([10, 1])

            with col1:
                if st.button(
                    f"📄 {relative_path}",
                    key=f"sel_{file_item.path}",
                    use_container_width=True,
                ):
                    st.session_state.app.selections.selected_file = file_item.path
                    st.rerun()

            with col2:
                if st.button(
                    "❌",
                    key=f"remove_{file_item.path}",
                    help=f"Remove {relative_path} from selection",
                ):
                    try:
                        file_item.toggle_selected()
                        show_temp_notification(
                            f"Removed {Path(file_item.path).name} from selection",
                            type="info",
                        )
                        # If we were viewing this file, clear it
                        if (
                            st.session_state.app.selections.selected_file
                            == file_item.path
                        ):
                            st.session_state.app.selections.selected_file = None
                        st.rerun()
                    except Exception as e:
                        logger.error(
                            f"Error removing file from selection: {e}", exc_info=True
                        )
                        show_temp_notification(
                            f"Error removing file: {str(e)}", type="error"
                        )
    else:
        show_temp_notification(
            "No files selected. Use the checkboxes in the file tree to select files.",
            type="info",
        )

    # Show file content if a file is selected
    if (
        st.session_state.app.selections.selected_file
        and st.session_state.app.selections.selected_file_content
    ):
        st.subheader(f"File: {st.session_state.app.selections.selected_file.name}")

        language = set_language_from_filename(
            st.session_state.app.selections.selected_file
        )

        st.code(
            st.session_state.app.selections.selected_file_content, language=language
        )
