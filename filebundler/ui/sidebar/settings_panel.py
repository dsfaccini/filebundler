# filebundler/ui/sidebar/settings_panel.py
import streamlit as st

from filebundler.ui.notification import show_temp_notification
from filebundler.managers.ProjectSettingsManager import ProjectSettingsManager


def render_settings_panel(psm: ProjectSettingsManager):
    # Only show settings when project is loaded
    if st.session_state.project_loaded:
        psm.project_settings.max_files = st.number_input(
            "Max files to display",
            min_value=10,
            value=psm.project_settings.max_files,
        )

        st.subheader("Ignore Patterns")
        st.write("Files matching these patterns will be ignored (glob syntax)")

        with st.expander("Show/Hide Ignore Patterns", expanded=False):
            updated_patterns = st.text_area(
                "Edit ignore patterns",
                "\n".join(psm.project_settings.ignore_patterns),
            )

            if updated_patterns:
                psm.project_settings.ignore_patterns = updated_patterns.split("\n")

        # Save button for all settings
        if st.button("Save Settings"):
            success = psm.save_project_settings()

            if success:
                show_temp_notification("Settings saved", type="success")
            else:
                show_temp_notification("Error saving settings", type="error")
    else:
        st.info("Open a project to configure settings")
