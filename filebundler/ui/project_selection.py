# filebundler/ui/project_selection.py
import os
import logging
import streamlit as st

from pathlib import Path

from filebundler.ui.notification import show_temp_notification

from filebundler.FileBundlerApp import FileBundlerApp

from filebundler.managers.BundleManager import BundleManager
from filebundler.managers.SettingsManager import SettingsManager

logger = logging.getLogger(__name__)


def load_project(
    project_path: str,
    app: FileBundlerApp,
    settings_manager: SettingsManager,
    bundle_manager: BundleManager,
):
    """Load a project and its settings"""

    if not project_path:
        show_temp_notification("Please enter a project path", type="error")
        return False

    project_path_obj = Path(project_path)
    if not project_path_obj.exists() or not project_path_obj.is_dir():
        logger.error(f"Invalid directory path: {project_path}")
        show_temp_notification("Invalid directory path", type="error")
        return False

    try:
        # Load project settings BEFORE loading the project
        # This ensures ignore patterns are available when loading the file tree
        settings_manager.load_project_settings(project_path)

        # Now load the project with the correct settings
        app.load_project(project_path)
        bundle_manager.set_project_path(project_path_obj)
        bundle_manager.load_bundles()
        st.session_state.project_loaded = True

        # Add to recent projects
        settings_manager.add_recent_project(project_path)

        logger.info(f"Project loaded: {project_path}")
        show_temp_notification(f"Project loaded: {project_path}", type="success")
        return True
    except Exception as e:
        logger.error(f"Error loading project: {e}", exc_info=True)
        show_temp_notification(f"Error loading project: {str(e)}", type="error")
        return False


def render_project_selection():
    """Render the project selection section"""
    st.subheader("Project")

    # Get recent projects
    recent_projects = st.session_state.settings_manager.get_recent_projects()

    # Initialize project path
    project_path = ""

    if recent_projects:
        project_source = st.radio(
            "Choose project source:",
            options=["Enter manually", "Select recent project"],
        )

        if project_source == "Select recent project":
            selected_recent = st.selectbox(
                "Recent projects:",
                options=recent_projects,
                format_func=lambda x: os.path.basename(x) + f" ({x})",
            )
            if selected_recent:
                project_path = selected_recent
        else:
            project_path = st.text_input(
                "Project Path",
                value=str(st.session_state.app.project_path)
                if st.session_state.project_loaded
                else "",
            )
    else:
        # No recent projects, just show the text input
        project_path = st.text_input(
            "Project Path",
            value=str(st.session_state.app.project_path)
            if st.session_state.project_loaded
            else "",
        )

    col1a, col1b = st.columns(2)
    with col1a:
        if st.button("Open Project"):
            load_project(
                project_path,
                st.session_state.app,
                st.session_state.settings_manager,
                st.session_state.bundle_manager,
            )
            st.rerun()

    with col1b:
        if st.button("Refresh Project"):
            if st.session_state.project_loaded:
                try:
                    st.session_state.app.load_project(st.session_state.app.project_path)
                    st.session_state.bundle_manager.load_bundles()
                    show_temp_notification("Project refreshed", type="success")
                except Exception as e:
                    logger.error(f"Error refreshing project: {e}", exc_info=True)
                    show_temp_notification(
                        f"Error refreshing project: {str(e)}", type="error"
                    )
            else:
                show_temp_notification("No project loaded", type="error")

    return project_path
