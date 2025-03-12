import os
import pyperclip
import streamlit as st

from pathlib import Path

from filebundler.FileBundlerApp import FileBundlerApp
from filebundler.settings_manager import SettingsManager
from filebundler.settings_panel import render_settings_panel
from filebundler.utils import show_temp_notification
from filebundler.constants import DEFAULT_IGNORE_PATTERNS


def load_project(project_path, app, settings_manager):
    """Load a project and its settings"""
    if not project_path:
        show_temp_notification("Please enter a project path", type="error")
        return False

    if not Path(project_path).exists() or not Path(project_path).is_dir():
        show_temp_notification("Invalid directory path", type="error")
        return False

    # Load project settings BEFORE loading the project
    # This ensures ignore patterns are available when loading the file tree
    project_settings = settings_manager.load_project_settings(project_path)
    st.session_state.ignore_patterns = project_settings["ignore_patterns"]
    st.session_state.max_files = project_settings["max_files"]

    # Now load the project with the correct settings
    app.load_project(project_path)
    app.load_bundles()
    st.session_state.project_loaded = True

    # Add to recent projects
    settings_manager.add_recent_project(project_path)

    show_temp_notification(f"Project loaded: {project_path}", type="success")
    return True


def main():
    st.set_page_config(page_title="File Bundler", layout="wide")

    # Initialize settings in session state
    if "ignore_patterns" not in st.session_state:
        st.session_state.ignore_patterns = DEFAULT_IGNORE_PATTERNS

    if "max_files" not in st.session_state:
        st.session_state.max_files = 500

    # Initialize session state
    if "app" not in st.session_state:
        st.session_state.app = FileBundlerApp()

    if "project_loaded" not in st.session_state:
        st.session_state.project_loaded = False

    if "file_content" not in st.session_state:
        st.session_state.file_content = None

    if "selected_file" not in st.session_state:
        st.session_state.selected_file = None

    if "settings_manager" not in st.session_state:
        st.session_state.settings_manager = SettingsManager()

    # SETTINGS SIDEBAR - Refactored into settings_panel.py
    with st.sidebar:
        render_settings_panel(st.session_state.settings_manager, st.session_state.app)

    # App header
    st.title("File Bundler")
    st.write(
        "Bundle project files together for prompting, or estimating and optimizing token and context usage."
    )

    # Two-column layout
    col1, col2 = st.columns([1, 2])

    with col1:
        # Add this inside the with col1: block, before displaying the file tree
        st.markdown(
            """
        <style>
        /* Create scrollable container for files tree */
        [data-testid="stVerticalBlock"]:has(div.row-widget.stCheckbox) {
            max-height: 70vh;
            overflow-y: auto;
            padding-right: 10px;
        }
        </style>
        """,
            unsafe_allow_html=True,
        )
        # Project selection section
        st.subheader("Project")

        # Recent projects dropdown with improved UX
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
                )
                st.rerun()

        with col1b:
            if st.button("Refresh Project"):
                if st.session_state.project_loaded:
                    st.session_state.app.load_project(st.session_state.app.project_path)
                    st.session_state.app.load_bundles()
                    show_temp_notification("Project refreshed", type="success")
                else:
                    show_temp_notification("No project loaded", type="error")

        # Only show file tree if project is loaded
        if st.session_state.project_loaded:
            # File Tree
            st.subheader("Files")

            # Display file tree with checkboxes
            def display_directory(directory_item, indent=0):
                for child in directory_item.children:
                    if child.is_dir:
                        # Directory entry
                        st.markdown(f"{'&nbsp;' * indent * 4}📁 **{child.name}**")
                        display_directory(child, indent + 1)
                    else:
                        # File entry with checkbox
                        is_selected = (
                            child.path in st.session_state.app.selected_file_paths
                        )

                        # Using checkbox for selection
                        new_state = st.checkbox(
                            f"{'&nbsp;' * indent * 4} {child.name}",
                            value=is_selected,
                            key=f"file_{child.path}",
                            help=f"Select {child.name} for bundling",
                        )

                        # Handle checkbox change
                        if new_state != is_selected:
                            st.session_state.app.toggle_file_selection(child.path)
                            # Force refresh
                            st.rerun()

            # Display the file tree starting from root
            root_item = st.session_state.app.file_items[
                st.session_state.app.project_path
            ]
            display_directory(root_item)

            # Button to clear all selections
            if st.button("Clear All Selections"):
                st.session_state.app.clear_all_selections()
                st.rerun()

    # Right column with bundle operations and file preview
    with col2:
        # Only show if project is loaded
        if st.session_state.project_loaded:
            # Tabs for different views
            tab1, tab2, tab3 = st.tabs(
                ["Selected Files", "Export Contents", "Manage Bundles"]
            )

            with tab1:
                st.subheader("Selected Files")
                st.text("Click on a file to view its content")

                # Get selected files
                selected_files = st.session_state.app.get_selected_files()

                if selected_files:
                    for file_item in selected_files:
                        relative_path = st.session_state.app.get_relative_path(
                            file_item.path
                        )
                        if st.button(
                            f"📄 {relative_path}", key=f"sel_{file_item.path}"
                        ):
                            st.session_state.selected_file = file_item.path
                            st.session_state.file_content = (
                                st.session_state.app.show_file_content(file_item.path)
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
                    st.code(st.session_state.file_content, language="python")

            with tab2:
                st.subheader("Export Contents")

                # Basic bundle creation
                if st.button("Export Contents"):
                    bundle_content = st.session_state.app.create_bundle()

                    if (
                        bundle_content.startswith("No files")
                        or bundle_content.startswith("The file")
                        or bundle_content.startswith("Failed to")
                    ):
                        show_temp_notification(bundle_content, type="error")
                    else:
                        st.session_state.bundle_content = bundle_content
                        pyperclip.copy(bundle_content)
                        # Success message
                        show_temp_notification(
                            f"Bundle created with {len(st.session_state.app.get_selected_files())} files",
                            type="success",
                        )

                # Save bundle with name
                col2a, col2b = st.columns([3, 1])
                with col2a:
                    bundle_name = st.text_input("Bundle Name (lowercase alphanumeric)")
                with col2b:
                    if st.button("Save Bundle"):
                        result = st.session_state.app.save_bundle(bundle_name)

                        if (
                            result.startswith("No files")
                            or result.startswith("Please")
                            or result.startswith("Bundle name")
                        ):
                            show_temp_notification(result, type="error")
                        else:
                            show_temp_notification(result, type="success")

                # Display the bundle content
                if "bundle_content" in st.session_state:
                    st.subheader("Bundle Preview")
                    st.text_area(
                        "Bundle Content", st.session_state.bundle_content, height=300
                    )

                    # Copy to clipboard button (note: this doesn't work in Streamlit cloud due to browser limitations)
                    if st.button("Copy to Clipboard"):
                        try:
                            pyperclip.copy(st.session_state.bundle_content)
                            show_temp_notification(
                                "Bundle copied to clipboard", type="success"
                            )
                        except Exception as e:
                            show_temp_notification(
                                f"Could not copy to clipboard: {str(e)}", type="error"
                            )
                            show_temp_notification(
                                "You can manually copy the content from the text area above",
                                type="info",
                            )

            with tab3:
                st.subheader("Manage Bundles")

                # List existing bundles
                if st.session_state.app.bundles:
                    st.write("Saved Bundles:")

                    for bundle in st.session_state.app.bundles:
                        col3a, col3b, col3c, col4c = st.columns([3, 1, 1, 1])

                        with col3a:
                            st.write(
                                f"**{bundle.name}** ({len(bundle.file_paths)} files)"
                            )

                        with col3b:
                            if st.button("Load", key=f"load_{bundle.name}"):
                                result = st.session_state.app.load_bundle(bundle.name)
                                show_temp_notification(result, type="success")
                                st.rerun()

                        with col3c:
                            if st.button("Export Content", key=f"export_{bundle.name}"):
                                bundle_content = (
                                    st.session_state.app.create_bundle_from_saved(
                                        bundle.name
                                    )
                                )

                                if (
                                    bundle_content.startswith("Bundle")
                                    or bundle_content.startswith("The file")
                                    or bundle_content.startswith("Failed to")
                                ):
                                    show_temp_notification(bundle_content, type="error")
                                else:
                                    try:
                                        pyperclip.copy(bundle_content)
                                        show_temp_notification(
                                            f"Bundle '{bundle.name}' exported to clipboard",
                                            type="success",
                                        )
                                    except Exception as e:
                                        show_temp_notification(
                                            f"Could not copy to clipboard: {str(e)}",
                                            type="error",
                                        )
                                        # Store content for manual copying
                                        st.session_state[
                                            f"export_content_{bundle.name}"
                                        ] = bundle_content
                                        st.rerun()

                        with col4c:
                            # Store confirmation state in session state
                            confirm_key = f"confirm_delete_{bundle.name}"

                            # If we're not in confirmation mode, show delete button
                            if confirm_key not in st.session_state:
                                if st.button("Delete", key=f"del_{bundle.name}"):
                                    # Enter confirmation mode
                                    st.session_state[confirm_key] = True
                                    st.rerun()
                            else:
                                # We're in confirmation mode, show confirm button
                                if st.button(
                                    "Confirm?",
                                    key=f"confirm_{bundle.name}",
                                    type="primary",
                                ):
                                    # Perform deletion
                                    result = st.session_state.app.delete_bundle(
                                        bundle.name
                                    )
                                    # Exit confirmation mode
                                    del st.session_state[confirm_key]
                                    show_temp_notification(result, type="success")
                                    st.rerun()

                        with st.expander(f"Files in {bundle.name}"):
                            for path in bundle.file_paths:
                                st.write(f"• {path}")

                            new_name = st.text_input(
                                "New name", key=f"rename_input_{bundle.name}"
                            )
                            if st.button("Rename", key=f"rename_{bundle.name}"):
                                if new_name and new_name != bundle.name:
                                    result = st.session_state.app.rename_bundle(
                                        bundle.name, new_name
                                    )
                                    if result.startswith("Successfully"):
                                        show_temp_notification(result, type="success")
                                    else:
                                        show_temp_notification(result, type="error")
                                    st.rerun()
                                else:
                                    show_temp_notification(
                                        "Please enter a new name different from the current one.",
                                        type="error",
                                    )
                else:
                    show_temp_notification("No saved bundles found", type="info")
        else:
            # If no project loaded
            show_temp_notification("Please open a project to get started", type="info")


if __name__ == "__main__":
    main()
