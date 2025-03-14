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
    st.subheader(f"Selected Files ({app.nr_of_selected_files})")
    st.text(
        "Click on a file to view its content. Click 'x' to remove a file from selection."
    )

    # Get selected files
    selected_files = app.get_selected_files()

    # TODO make this section scrollable, set a max height
    if selected_files:
        for file_item in selected_files:
            relative_path = file_item.path.relative_to(app.project_path)

            # Create a row with file button and remove button
            col1, col2 = st.columns([10, 1])

            with col1:
                if st.button(
                    f"📄 {relative_path}",
                    key=f"sel_{file_item.path}",
                    use_container_width=True,
                ):
                    st.session_state.selected_file = file_item.path
                    st.session_state.file_content = app.show_file_content(
                        file_item.path
                    )
                    st.rerun()

            with col2:
                if st.button(
                    "❌",
                    key=f"remove_{file_item.path}",
                    help=f"Remove {relative_path} from selection",
                ):
                    try:
                        app.toggle_file_selection(file_item.path)
                        show_temp_notification(
                            f"Removed {Path(file_item.path).name} from selection",
                            type="info",
                        )
                        # If we were viewing this file, clear it
                        if st.session_state.selected_file == file_item.path:
                            st.session_state.selected_file = None
                            st.session_state.file_content = None
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
    if st.session_state.selected_file and st.session_state.file_content:
        st.subheader(f"File: {Path(st.session_state.selected_file).name}")

        filepath = Path(st.session_state.selected_file)
        language = set_language_from_filename(filepath)

        st.code(st.session_state.file_content, language=language)
