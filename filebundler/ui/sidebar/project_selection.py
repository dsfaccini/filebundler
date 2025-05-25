# filebundler/ui/sidebar/project_selection.py
import os
import logging
import streamlit as st

from pathlib import Path

from filebundler.constants import DISPLAY_NR_OF_RECENT_PROJECTS

from filebundler.ui.notification import show_temp_notification
from filebundler.ui.components.path_migration_dialog import render_path_migration_dialog, render_path_validation_warning

from filebundler.services.project_structure import save_project_structure

from filebundler.FileBundlerApp import FileBundlerApp
from filebundler.models.GlobalSettings import GlobalSettings


logger = logging.getLogger(__name__)


def open_selected_project(project_path: str):
    """Load a project and its settings"""

    project_path_obj = Path(project_path)
    if not project_path_obj.exists() or not project_path_obj.is_dir():
        logger.error(f"Invalid directory path: {project_path}")
        show_temp_notification("Invalid directory path", type="error")
        return False

    try:
        # Load project settings BEFORE loading the project
        # This ensures ignore patterns are available when loading the file tree
        app = FileBundlerApp(project_path=project_path_obj)
        
        # Check for path validation issues and handle them
        if hasattr(app, 'path_validation_result') and not app.path_validation_result.is_valid:
            # Show path migration dialog if there are validation issues
            new_path = render_path_migration_dialog(
                app.path_validation_result, 
                app.psm.filebundler_dir
            )
            
            if new_path:
                # User chose to update the path
                success = app.update_project_path_if_needed(new_path)
                if success:
                    show_temp_notification("Project path updated successfully!", type="success")
                else:
                    show_temp_notification("Failed to update project path", type="error")
                    return False
            else:
                # User didn't resolve the issue, but we'll continue with a warning
                render_path_validation_warning(app.path_validation_result)
        
        st.session_state.app = app

        # Add to recent projects
        st.session_state.global_settings_manager.add_recent_project(app.project_path)

        logger.info(f"Project loaded: {app.project_path}")
        show_temp_notification(f"Project loaded: {app.project_path}", type="success")

        save_project_structure(app)
        return True
    except Exception as e:
        logger.error(f"Error loading project: {e}", exc_info=True)
        show_temp_notification(f"Error loading project: {str(e)}", type="error")
        return False


def render_project_selection(global_settings: GlobalSettings):
    """Render the project selection section"""
    project_path = ""
    with st.expander("Select Project", expanded=not st.session_state.app):
        if global_settings.recent_projects:
            project_source = st.radio(
                "Choose project source:",
                options=["Select recent project", "Enter manually"],
            )

            if project_source == "Select recent project":
                selected_recent: str = st.selectbox(
                    "Recent projects:",
                    options=global_settings.recent_projects_str[
                        :DISPLAY_NR_OF_RECENT_PROJECTS
                    ],
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
            project_path_input = st.text_input(
                "Project Path",
                value="",
            )
            if project_path_input:
                project_path = project_path_input

        if st.button("Open Project") and project_path:
            open_selected_project(project_path)
            st.rerun()
    
    # Show path validation warning for already loaded projects
    if st.session_state.app and hasattr(st.session_state.app, 'path_validation_result'):
        if not st.session_state.app.path_validation_result.is_valid:
            render_path_validation_warning(st.session_state.app.path_validation_result)
