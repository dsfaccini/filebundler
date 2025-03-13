# filebundler/ui/sidebar/settings_panel.py

import streamlit as st

from typing import List

from filebundler.FileBundlerApp import FileBundlerApp
from filebundler.managers.SettingsManager import SettingsManager

from filebundler.ui.notification import show_temp_notification


def render_settings_panel(app: FileBundlerApp, settings_manager: SettingsManager):
    """Render the settings sidebar panel"""

    st.header("Settings")

    # Only show settings when project is loaded
    if st.session_state.project_loaded:
        settings_manager.project_settings.max_files = st.number_input(
            "Max files to display",
            min_value=10,
            value=settings_manager.project_settings.max_files,
        )

        st.subheader("Ignore Patterns")
        st.write("Files matching these patterns will be ignored (glob syntax)")

        with st.expander("Show/Hide Ignore Patterns", expanded=False):
            updated_patterns: List[str] = []

            for i, pattern in enumerate(
                settings_manager.project_settings.ignore_patterns
            ):
                cols = st.columns([4, 1])
                with cols[0]:
                    updated_pattern = st.text_input(
                        f"Pattern {i + 1}", value=pattern, key=f"pat_{i}"
                    )
                    updated_patterns.append(updated_pattern)
                with cols[1]:
                    if st.button("❌", key=f"del_pat_{i}"):
                        settings_manager.project_settings.ignore_patterns.pop(i)

                        # Save settings after change
                        if st.session_state.project_loaded:
                            settings_manager.save_project_settings(app.project_path)

                        st.rerun()

        settings_manager.project_settings.ignore_patterns = updated_patterns

        # Add new pattern
        new_pattern = st.text_input("Add new pattern")
        if st.button("Add") and new_pattern:
            settings_manager.project_settings.ignore_patterns.append(new_pattern)

            # Save settings after adding new pattern
            if st.session_state.project_loaded:
                settings_manager.save_project_settings(app.project_path)

            st.rerun()

        # Update patterns with edited values
        settings_manager.project_settings.ignore_patterns = updated_patterns

        # Save button for all settings
        if st.button("Save Settings"):
            if st.session_state.project_loaded:
                settings_manager.save_project_settings(app.project_path)

                success = settings_manager.save_project_settings(app.project_path)

                if success:
                    show_temp_notification("Settings saved", type="success")
                else:
                    show_temp_notification("Error saving settings", type="error")
    else:
        st.info("Open a project to configure settings")
