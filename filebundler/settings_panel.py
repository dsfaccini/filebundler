# filebundler/settings_panel.py

import streamlit as st

from filebundler.FileBundlerApp import FileBundlerApp
from filebundler.settings_manager import SettingsManager
from filebundler.ui.notification import show_temp_notification


def render_settings_panel(settings_manager: SettingsManager, app: FileBundlerApp):
    """Render the settings sidebar panel"""

    st.header("Settings")

    # Only show settings when project is loaded
    if st.session_state.project_loaded:
        st.session_state.max_files = st.number_input(
            "Max files to display", min_value=10, value=st.session_state.max_files
        )

        st.subheader("Ignore Patterns")
        st.write("Files matching these patterns will be ignored (glob syntax)")

        with st.expander("Show/Hide Ignore Patterns", expanded=False):
            updated_patterns = []

            for i, pattern in enumerate(st.session_state.ignore_patterns):
                cols = st.columns([4, 1])
                with cols[0]:
                    updated_pattern = st.text_input(
                        f"Pattern {i + 1}", value=pattern, key=f"pat_{i}"
                    )
                    updated_patterns.append(updated_pattern)
                with cols[1]:
                    if st.button("❌", key=f"del_pat_{i}"):
                        st.session_state.ignore_patterns.pop(i)

                        # Save settings after change
                        if st.session_state.project_loaded:
                            settings = {
                                "ignore_patterns": st.session_state.ignore_patterns,
                                "max_files": st.session_state.max_files,
                            }
                            settings_manager.save_project_settings(
                                app.project_path, settings
                            )

                        st.rerun()

        st.session_state.ignore_patterns = updated_patterns

        # Add new pattern
        new_pattern = st.text_input("Add new pattern")
        if st.button("Add") and new_pattern:
            st.session_state.ignore_patterns.append(new_pattern)

            # Save settings after adding new pattern
            if st.session_state.project_loaded:
                settings = {
                    "ignore_patterns": st.session_state.ignore_patterns,
                    "max_files": st.session_state.max_files,
                }
                settings_manager.save_project_settings(app.project_path, settings)

            st.rerun()

        # Update patterns with edited values
        st.session_state.ignore_patterns = updated_patterns

        # Save button for all settings
        if st.button("Save Settings"):
            if st.session_state.project_loaded:
                settings = {
                    "ignore_patterns": st.session_state.ignore_patterns,
                    "max_files": st.session_state.max_files,
                }
                success = settings_manager.save_project_settings(
                    app.project_path, settings
                )

                if success:
                    show_temp_notification("Settings saved", type="success")
                else:
                    show_temp_notification("Error saving settings", type="error")
    else:
        st.info("Open a project to configure settings")
