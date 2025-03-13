# filebundler/FileBundlerApp.py
import re
import json
import logging
import fnmatch
import streamlit as st

from pathlib import Path
from typing import Dict, List, Optional, Set, Tuple

from filebundler.models.Bundle import Bundle
from filebundler.utils import json_dump, make_file_section
from filebundler.ui.notification import show_temp_notification

logger = logging.getLogger(__name__)


class FileItem:
    def __init__(self, path: Path, is_dir: bool = False, parent=None):
        self.path = path
        self.name = path.name
        self.is_dir = is_dir
        self.parent = parent
        self.children = []
        self.selected = False

    def __repr__(self):
        return f"FileItem({self.path}, is_dir={self.is_dir})"


class FileBundlerApp:
    def __init__(self):
        self.project_path = Path()
        self.file_items: Dict[Path, FileItem] = {}
        self.selected_file_paths: Set[Path] = set()
        self.selected_file_content: Optional[str] = None
        self.bundles: List[Bundle] = []

    @property
    def nr_of_selected_files(self):
        return len(self.selected_file_paths)

    @property
    def nr_of_bundles(self):
        return len(self.bundles)

    def load_project(self, project_path: str):
        """Load a project directory"""
        self.project_path = Path(project_path)
        self.file_items = {}
        self.selected_file_paths = set()

        # Load the root directory
        root_item = FileItem(self.project_path, is_dir=True)
        self.file_items[self.project_path] = root_item

        # Load the directory structure
        self.load_directory_recursive(self.project_path, root_item)

        # Load saved selections for this project if exists
        self.load_selections()

        # Load saved bundles
        self.load_bundles()

    def ignore_patterns(self, item_path: Path) -> bool:
        """Check if file matches any ignore patterns"""
        return any(
            fnmatch.fnmatch(str(item_path.relative_to(self.project_path)), pattern)
            for pattern in st.session_state.settings_manager.project_settings.ignore_patterns
        )

    def sort_files(self, files: List[Path]) -> List[Path]:
        """Sort files alphabetically"""
        return sorted(files, key=lambda p: (not p.is_dir(), p.name.lower()))

    def load_directory_recursive(self, dir_path: Path, parent_item: FileItem) -> bool:
        """
        Recursively load directory structure

        Returns:
            bool: True if the directory or any of its subdirectories contains visible files,
                False if the directory is empty or all its files are ignored
        """
        try:
            # Filter items based on ignore patterns
            filtered_items = [
                item for item in dir_path.iterdir() if not self.ignore_patterns(item)
            ]
            if (
                len(filtered_items)
                > st.session_state.settings_manager.project_settings.max_files
            ):
                st.warning(
                    f"Directory contains {len(filtered_items)} files which exceeds the limit of {st.session_state.settings_manager.project_settings.max_files}. Some files may not be displayed."
                )
                items = self.sort_files(filtered_items)[
                    : st.session_state.settings_manager.project_settings.max_files
                ]
            else:
                items = self.sort_files(filtered_items)

            # Track if this directory contains any visible files or non-empty subdirectories
            has_visible_content = False

            for item_path in items:
                try:
                    if item_path.is_dir():
                        # Create file item
                        file_item = FileItem(item_path, is_dir=True, parent=parent_item)
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
                        file_item = FileItem(item_path, parent=parent_item)
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

    def toggle_file_selection(self, file_path: Path):
        """Toggle selection state of a file"""
        if file_path in self.file_items:
            file_item = self.file_items[file_path]
            if not file_item.is_dir:
                file_item.selected = not file_item.selected

                if file_item.selected:
                    self.selected_file_paths.add(file_path)
                else:
                    self.selected_file_paths.discard(file_path)

                # Save selections to file
                self.save_selections()
                return True
        return False

    def clear_all_selections(self):
        """Clear all selected files"""
        for path, file_item in self.file_items.items():
            if not file_item.is_dir:
                file_item.selected = False

        self.selected_file_paths.clear()

        # Save empty selections
        self.save_selections()

    def get_selected_files(self) -> List[FileItem]:
        """Get all selected files"""
        return [
            self.file_items[path]
            for path in self.selected_file_paths
            if path in self.file_items
        ]

    def get_selected_file_paths(self) -> List[str]:
        """Get paths of all selected files as strings"""
        return [str(path) for path in self.selected_file_paths]

    def get_relative_path(self, file_path: Path) -> str:
        """Get path relative to project root"""
        try:
            return str(file_path.relative_to(self.project_path).as_posix())
        except ValueError:
            # If the file is not in the project directory, return the full path
            return str(file_path)

    def _read_file_content(
        self, file_path: Path, relative_path: str
    ) -> Tuple[str, bool]:
        """Read file content with error handling

        Returns:
            tuple: (content_or_error_message, success_flag)
        """
        try:
            # Check if file exists
            if not file_path.exists():
                return (
                    f"The file {relative_path} does not exist or cannot be accessed.",
                    False,
                )

            # Read file content
            try:
                file_content = file_path.read_text(encoding="utf-8", errors="replace")
                return file_content, True
            except UnicodeDecodeError:
                return (
                    f"Could not read {file_path.name} as text. It may be a binary file.",
                    False,
                )

        except Exception as e:
            return f"Failed to read {relative_path}: {str(e)}", False

    def _generate_bundle_content(self, file_paths: List[Path]) -> str:
        """Generate bundle content from a list of file paths

        Returns:
            str: Generated bundle or error message
        """
        if not file_paths:
            return "No files provided. Please select files to bundle."

        bundle_content = []

        for file_path in file_paths:
            relative_path = self.get_relative_path(file_path)
            content, success = self._read_file_content(file_path, relative_path)

            if not success:
                return content  # This is an error message

            bundle_content.append(make_file_section(relative_path, content))

        # Join all content
        return "\n".join(bundle_content)

    def create_bundle(self) -> str:
        """Create a bundle from selected files"""
        selected_files = self.get_selected_files()
        if not selected_files:
            return "No files selected. Please select files to bundle."

        file_paths = [file_item.path for file_item in selected_files]
        return self._generate_bundle_content(file_paths)

    def create_bundle_from_saved(self, bundle_name: str) -> str:
        """Create a bundle from a saved bundle without loading it"""
        # Find the bundle
        bundle = None
        for b in self.bundles:
            if b.name == bundle_name:
                bundle = b
                break

        if not bundle:
            return f"Bundle '{bundle_name}' not found."

        # Convert relative paths to full paths
        file_paths = [self.project_path / rel_path for rel_path in bundle.file_paths]
        return self._generate_bundle_content(file_paths)

    def _save_json_data(self, filename: str, data) -> bool:
        """Save data to JSON file in .filebundler directory

        Returns:
            bool: True if successful, False otherwise
        """
        try:
            # Create .filebundler directory if it doesn't exist
            bundle_dir = self.project_path / ".filebundler"
            bundle_dir.mkdir(exist_ok=True)

            file_path = bundle_dir / filename

            # Write to file
            with open(file_path, "w") as f:
                json_dump(data, f)
            return True

        except Exception as e:
            st.error(f"Error saving {filename}: {str(e)}")
            return False

    def _load_json_data(self, filename: str) -> Optional[dict]:
        """Load data from JSON file in .filebundler directory

        Returns:
            Optional[dict]: Loaded data or None if error
        """
        file_path = self.project_path / ".filebundler" / filename

        if not file_path.exists():
            return None

        try:
            with open(file_path, "r") as f:
                return json.load(f)
        except Exception as e:
            st.error(f"Error loading {filename}: {str(e)}")
            return None

    def save_bundle(self, bundle_name: str) -> str:
        """Save current selection as a named bundle"""
        selected_files = self.get_selected_files()
        if not selected_files:
            return "No files selected. Please select files to save as a bundle."

        if not bundle_name:
            return "Please enter a valid bundle name."

        # Check if name is valid (lowercase alphanumeric)
        if not re.fullmatch(r"[a-z0-9-]+", bundle_name):
            return (
                "Bundle name must be lowercase, alphanumeric, and may include hyphens."
            )

        # Check for duplicate names
        for b in self.bundles:
            if b.name == bundle_name:
                # Remove existing bundle with same name
                self.bundles = [b for b in self.bundles if b.name != bundle_name]
                break

        # Create new bundle
        file_paths = [self.get_relative_path(item.path) for item in selected_files]
        new_bundle = Bundle(bundle_name, file_paths)
        self.bundles.append(new_bundle)

        # Save bundles to file
        self.save_bundles()

        return f"Bundle '{bundle_name}' saved with {len(file_paths)} files."

    def load_bundle(self, bundle_name: str) -> str:
        """Load a saved bundle"""
        # Find the bundle
        bundle = None
        for b in self.bundles:
            if b.name == bundle_name:
                bundle = b
                break

        if not bundle:
            return f"Bundle '{bundle_name}' not found."

        # Clear current selections
        self.clear_all_selections()

        # Mark selected files
        loaded_count = 0
        for rel_path in bundle.file_paths:
            try:
                full_path = self.project_path / rel_path

                if full_path in self.file_items:
                    file_item = self.file_items[full_path]
                    file_item.selected = True
                    self.selected_file_paths.add(full_path)
                    loaded_count += 1
            except Exception as e:
                st.error(f"Error loading path {rel_path}: {str(e)}")

        # Save selections
        self.save_selections()

        return f"Loaded {loaded_count} of {len(bundle.file_paths)} files from bundle '{bundle_name}'."

    def delete_bundle(self, bundle_name: str) -> str:
        """Delete a saved bundle"""
        for i, bundle in enumerate(self.bundles):
            if bundle.name == bundle_name:
                self.bundles.pop(i)
                self.save_bundles()
                return f"Bundle '{bundle_name}' has been deleted."

        return f"Bundle '{bundle_name}' not found."

    def save_selections(self):
        """Save selected files to JSON file"""
        if not self.project_path.exists():
            return

        # Create data structure with project path and selected files
        data = {
            "project": str(self.project_path),
            "selections": self.get_selected_file_paths(),
        }

        # Save to file
        self._save_json_data("selections.json", data)

    def load_selections(self):
        """Load selected files from JSON file"""
        data = self._load_json_data("selections.json")
        if not data:
            return

        # Check if the loaded data is for the current project
        if data.get("project") != str(self.project_path):
            return

        # Set selections
        for path_str in data.get("selections", []):
            try:
                path = Path(path_str)
                if path in self.file_items:
                    file_item = self.file_items[path]
                    file_item.selected = True
                    self.selected_file_paths.add(path)
            except Exception as e:
                st.error(f"Error restoring selection for {path_str}: {str(e)}")

    def save_bundles(self):
        """Save bundles to file"""
        # Convert bundles to dictionary
        data = [
            {"name": bundle.name, "file_paths": bundle.file_paths}
            for bundle in self.bundles
        ]

        # Save to file
        self._save_json_data("bundles.json", data)

    def load_bundles(self):
        """Load bundles from file"""
        data = self._load_json_data("bundles.json")
        if not data:
            return

        # Convert to Bundle objects
        self.bundles = [Bundle.model_validate(item) for item in data]

    def show_file_content(self, file_path: Path) -> str:
        """Return file content for display"""
        content, success = self._read_file_content(file_path, str(file_path))
        return content

    def rename_bundle(self, old_name: str, new_name: str) -> str:
        """Rename a saved bundle"""
        # Find the bundle
        for bundle in self.bundles:
            if bundle.name == old_name:
                bundle.name = new_name
                self.save_bundles()
                return f"Bundle '{old_name}' renamed to '{new_name}'."

        return f"Bundle '{old_name}' not found."

    def select_all_files(self):
        """Select all files in the project"""
        try:
            selected_count = 0

            # Recursive function to select all files in a directory
            def select_all_in_dir(directory_item):
                nonlocal selected_count

                for child in directory_item.children:
                    if child.is_dir:
                        select_all_in_dir(child)
                    else:
                        if not child.selected:
                            child.selected = True
                            self.selected_file_paths.add(child.path)
                            selected_count += 1

            # Start from root directory
            root_item = self.file_items[self.project_path]
            select_all_in_dir(root_item)

            # Save selections
            self.save_selections()

            logger.info(f"Selected all {selected_count} files")
            show_temp_notification(
                f"Selected all {selected_count} files", type="success"
            )
        except Exception as e:
            logger.error(f"Error selecting all files: {e}", exc_info=True)
            show_temp_notification(f"Error selecting all files: {str(e)}", type="error")

    def unselect_all_files(self):
        """Unselect all files"""
        try:
            count = len(self.selected_file_paths)
            self.clear_all_selections()
            logger.info(f"Unselected all {count} files")
            show_temp_notification(f"Unselected all {count} files", type="success")
        except Exception as e:
            logger.error(f"Error unselecting all files: {e}", exc_info=True)
            show_temp_notification(
                f"Error unselecting all files: {str(e)}", type="error"
            )
