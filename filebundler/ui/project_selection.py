# filebundler/ui/project_selection.py
import os
import logging
import streamlit as st

from pathlib import Path

from filebundler.FileBundlerApp import FileBundlerApp

from filebundler.managers.SettingsManager import SettingsManager

from filebundler.ui.notification import show_temp_notification

logger = logging.getLogger(__name__)


def load_project(
    app: FileBundlerApp,
    settings_manager: SettingsManager,
    project_path: str,
):
    """Load a project and its settings"""

    # if app is None:
    #     show_temp_notification("Please enter a project path", type="error")
    #     return False

    project_path_obj = Path(project_path)
    if not project_path_obj.exists() or not project_path_obj.is_dir():
        logger.error(f"Invalid directory path: {project_path}")
        show_temp_notification("Invalid directory path", type="error")
        return False

    try:
        # Load project settings BEFORE loading the project
        # This ensures ignore patterns are available when loading the file tree
        settings_manager.load_project_settings(project_path_obj)

        # Now load the project with the correct settings
        app.load_project(project_path_obj, settings_manager.project_settings)
        st.session_state.project_loaded = True

        # Add to recent projects
        settings_manager.add_recent_project(app.project_path)

        logger.info(f"Project loaded: {app.project_path}")
        show_temp_notification(f"Project loaded: {app.project_path}", type="success")
        return True
    except Exception as e:
        logger.error(f"Error loading project: {e}", exc_info=True)
        show_temp_notification(f"Error loading project: {str(e)}", type="error")
        return False


def render_project_selection(app: FileBundlerApp, settings_manager: SettingsManager):
    """Render the project selection section"""
    project_path = ""
    with st.expander("Select Project", expanded=True):
        if settings_manager.recent_projects:
            project_source = st.radio(
                "Choose project source:",
                options=["Select recent project", "Enter manually"],
            )

            if project_source == "Select recent project":
                selected_recent = st.selectbox(
                    "Recent projects:",
                    options=settings_manager.recent_projects,
                    format_func=lambda x: os.path.basename(x) + f" ({x})",
                )
                if selected_recent:
                    project_path = selected_recent
            else:
                explicit_project_path = st.text_input(
                    "Project Path",
                    value="",
                )
                if explicit_project_path:
                    project_path = explicit_project_path
        else:
            # No recent projects, just show the text input
            project_path = st.text_input(
                "Project Path",
                value="",
            )
            if project_path:
                project_path = project_path

        if st.button("Open Project"):
            load_project(
                app,
                settings_manager,
                project_path,
            )
            st.rerun()
