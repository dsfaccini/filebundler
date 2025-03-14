# filebundler/FileBundlerApp.py
import logging
import streamlit as st

from typing import Dict
from pathlib import Path

from filebundler.models.FileItem import FileItem
from filebundler.managers.BundleManager import BundleManager
from filebundler.managers.SelectionsManager import SelectionsManager

from filebundler.utils import ignore_patterns, sort_files

logger = logging.getLogger(__name__)


class FileBundlerApp:
    def __init__(self):
        self.project_path = Path()
        self.file_items: Dict[Path, FileItem] = {}
        self.bundles = BundleManager()
        self.selections = SelectionsManager(self.project_path)

    @property
    def nr_of_selected_files(self):
        return self.selections.nr_of_selected_files

    @property
    def nr_of_bundles(self):
        return len(self.bundles.bundles)

    def load_project(self, project_path: str):
        """Load a project directory"""
        self.project_path = Path(project_path)
        self.file_items = {}

        # Update SelectionsManager with new project path
        self.selections = SelectionsManager(self.project_path)

        # Load the root directory
        root_item = FileItem(self.project_path)
        self.file_items[self.project_path] = root_item

        # Load the directory structure
        self.load_directory_recursive(self.project_path, root_item)

        # Update SelectionsManager with file_items
        self.selections.set_file_items(self.file_items)

        # Load saved selections for this project if exists
        self.selections.load_selections()

        # Initialize the bundle manager with the project path
        self.bundles.set_project_path(self.project_path)

    def load_directory_recursive(self, dir_path: Path, parent_item: FileItem):
        """
        Recursively load directory structure

        Returns:
            bool: True if the directory or any of its subdirectories contains visible files,
                False if the directory is empty or all its files are ignored
        """
        try:
            # Filter items based on ignore patterns
            filtered_items = [
                item
                for item in dir_path.iterdir()
                if not ignore_patterns(
                    item.relative_to(self.project_path).as_posix(),
                    st.session_state.settings_manager.project_settings.ignore_patterns,
                )
            ]
            if (
                len(filtered_items)
                > st.session_state.settings_manager.project_settings.max_files
            ):
                st.warning(
                    f"Directory contains {len(filtered_items)} files which exceeds the limit of {st.session_state.settings_manager.project_settings.max_files}. Some files may not be displayed."
                )
                items = sort_files(filtered_items)[
                    : st.session_state.settings_manager.project_settings.max_files
                ]
            else:
                items = sort_files(filtered_items)

            # Track if this directory contains any visible files or non-empty subdirectories
            has_visible_content = False

            for item_path in items:
                try:
                    if item_path.is_dir():
                        # Create file item
                        file_item = FileItem(item_path)
                        self.file_items[item_path] = file_item

                        # Recursively load subdirectory and check if it has visible content
                        subdirectory_has_content = self.load_directory_recursive(
                            item_path, file_item
                        )

                        # Only add non-empty directories to the tree
                        if subdirectory_has_content:
                            parent_item.children.append(file_item)
                            has_visible_content = True
                        else:
                            # Remove the empty directory from file_items
                            del self.file_items[item_path]

                    elif item_path.is_file():
                        # Create file item
                        file_item = FileItem(item_path)
                        self.file_items[item_path] = file_item
                        parent_item.children.append(file_item)
                        has_visible_content = True
                except (PermissionError, OSError) as e:
                    # Skip files/directories we can't access
                    continue

            return has_visible_content

        except Exception as e:
            st.error(f"Error loading directory {dir_path}: {str(e)}")
            return False  # Assume no content on error

    # Delegate selection methods to SelectionsManager
    def toggle_file_selection(self, file_path: Path):
        """Delegate to SelectionsManager"""
        return self.selections.toggle_file_selection(file_path)

    def clear_all_selections(self):
        """Delegate to SelectionsManager"""
        self.selections.clear_all_selections()

    def get_selected_files(self):
        """Delegate to SelectionsManager"""
        return self.selections.get_selected_files()

    def show_file_content(self, file_path: Path):
        """Delegate to SelectionsManager"""
        return self.selections.show_file_content(file_path)

    def save_selections(self):
        """Delegate to SelectionsManager"""
        self.selections.save_selections()

    def load_selections(self):
        """Delegate to SelectionsManager"""
        self.selections.load_selections()

    def select_all_files(self):
        """Delegate to SelectionsManager"""
        self.selections.select_all_files()

    def unselect_all_files(self):
        """Delegate to SelectionsManager"""
        self.selections.unselect_all_files()
