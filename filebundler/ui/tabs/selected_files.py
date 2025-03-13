# filebundler/ui/tabs/selected_files.py
import streamlit as st

from pathlib import Path

from filebundler.ui.notification import show_temp_notification
from filebundler.utils.language_formatting import set_language_from_filename


def render_selected_files_tab():
    """Render the Selected Files tab"""
    st.subheader(f"Selected Files ({st.session_state.app.nr_of_selected_files})")
    st.text("Click on a file to view its content")

    # Get selected files
    selected_files = st.session_state.app.get_selected_files()

    if selected_files:
        for file_item in selected_files:
            relative_path = st.session_state.app.get_relative_path(file_item.path)
            if st.button(f"📄 {relative_path}", key=f"sel_{file_item.path}"):
                st.session_state.selected_file = file_item.path
                st.session_state.file_content = st.session_state.app.show_file_content(
                    file_item.path
                )
                st.rerun()
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
