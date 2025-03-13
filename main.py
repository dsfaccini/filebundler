# main.py
import os
import logging
import streamlit as st

from pathlib import Path

from filebundler.BundleManager import BundleManager
from filebundler.FileBundlerApp import FileBundlerApp
from filebundler.constants import DEFAULT_IGNORE_PATTERNS

from filebundler.ui.tabs.export_contents import render_export_tab
from filebundler.ui.tabs.selected_files import render_selected_files_tab

from filebundler.ui.sidebar.settings_manager import SettingsManager
from filebundler.ui.sidebar.settings_panel import render_settings_panel

from filebundler.ui.file_tree import render_file_tree
from filebundler.ui.SelectionManager import SelectionManager
from filebundler.ui.tabs.manage_bundles import render_manage_bundles_tab
from filebundler.ui.notification import show_temp_notification

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


def load_project(project_path, app, settings_manager, bundle_manager):
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
        project_settings = settings_manager.load_project_settings(project_path)
        st.session_state.ignore_patterns = project_settings["ignore_patterns"]
        st.session_state.max_files = project_settings["max_files"]

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


def initialize_session_state():
    """Initialize all session state variables"""
    # Settings
    if "ignore_patterns" not in st.session_state:
        st.session_state.ignore_patterns = DEFAULT_IGNORE_PATTERNS

    if "max_files" not in st.session_state:
        st.session_state.max_files = 500

    # App state
    if "app" not in st.session_state:
        st.session_state.app = FileBundlerApp()

    if "bundle_manager" not in st.session_state:
        st.session_state.bundle_manager = BundleManager()

    if "settings_manager" not in st.session_state:
        st.session_state.settings_manager = SettingsManager()

    # UI state
    if "project_loaded" not in st.session_state:
        st.session_state.project_loaded = False

    if "file_content" not in st.session_state:
        st.session_state.file_content = None

    if "selected_file" not in st.session_state:
        st.session_state.selected_file = None

    # Add selection manager
    if "selection_manager" not in st.session_state:
        st.session_state.selection_manager = SelectionManager()


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


def main():
    try:
        st.set_page_config(page_title="File Bundler", layout="wide")

        # Initialize session state
        initialize_session_state()

        # Configure sidebar
        with st.sidebar:
            render_settings_panel(
                st.session_state.settings_manager, st.session_state.app
            )

        # App header
        st.title("File Bundler")
        st.write(
            "Bundle project files together for prompting, or estimating and optimizing token and context usage."
        )

        # Two-column layout
        col1, col2 = st.columns([1, 2])

        with col1:
            # Project selection section
            project_path = render_project_selection()

            # Only show file tree if project is loaded
            if st.session_state.project_loaded:
                # Render the file tree
                render_file_tree(
                    st.session_state.app.file_items,
                    st.session_state.app.project_path,
                    st.session_state.app.selected_file_paths,
                    st.session_state.app.toggle_file_selection,
                    st.session_state.app.select_all_files,  # Add this function to FileBundlerApp
                    st.session_state.app.unselect_all_files,  # Add this function to FileBundlerApp
                )

        # Right column with bundle operations and file preview
        with col2:
            # Only show if project is loaded
            if st.session_state.project_loaded:
                # Tabs for different views
                tab1, tab2, tab3 = st.tabs(
                    [
                        f"Selected Files ({st.session_state.app.nr_of_selected_files})",
                        "Export Contents",
                        f"Manage Bundles ({st.session_state.app.nr_of_bundles})",
                    ]
                )

                with tab1:
                    render_selected_files_tab()

                with tab2:
                    render_export_tab()

                with tab3:
                    render_manage_bundles_tab()
            else:
                # If no project loaded
                show_temp_notification(
                    "Please open a project to get started", type="info"
                )

    except Exception as e:
        logger.error(f"Application error: {e}", exc_info=True)
        st.error(f"An error occurred: {str(e)}")


if __name__ == "__main__":
    main()
