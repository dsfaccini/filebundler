# filebundler/managers/SelectionsManager.py
import json
import logging

from pathlib import Path
from typing import Dict, List, Optional, Set

from filebundler.models.FileItem import FileItem
from filebundler.ui.notification import show_temp_notification
from filebundler.utils import json_dump, read_file

logger = logging.getLogger(__name__)


class SelectionsManager:
    """
    Manages the state of selected files and file selections persistence
    """

    def __init__(self, project_path: Path, file_items: Dict[Path, FileItem] = None):
        self.project_path = project_path
        self.file_items = file_items or {}
        self.selected_file_paths: Set[Path] = set()
        self.selected_file: Optional[Path] = None

    @property
    def selected_file_content(self):
        """Return the content of the selected file"""
        if self.selected_file:
            return read_file(self.selected_file)

    @property
    def nr_of_selected_files(self):
        """Return the number of selected files"""
        return len(self.selected_file_paths)

    def set_file_items(self, file_items: Dict[Path, FileItem]):
        """Set the file items dictionary"""
        self.file_items = file_items

    def toggle_file_selection(self, file_path: Path):
        """
        Toggle selection state of a file

        Args:
            file_path: Path to the file to toggle

        Returns:
            bool: True if the toggle was successful, False otherwise
        """
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
        self.save_selections()

    def get_selected_files(self):
        """Get all selected files as FileItem objects"""
        return [
            self.file_items[path]
            for path in self.selected_file_paths
            if path in self.file_items
        ]

    def _read_file_content(self, file_path: Path, relative_path: str):
        """
        Read file content with error handling

        Args:
            file_path: Path to the file to read
            relative_path: Relative path for error messages

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

    def _save_json_data(self, filename: str, data):
        """
        Save data to JSON file in .filebundler directory

        Args:
            filename: Name of the file to save
            data: Data to save

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
            logger.error(f"Error saving {filename}: {str(e)}", exc_info=True)
            return False

    def _load_json_data(self, filename: str):
        """
        Load data from JSON file in .filebundler directory

        Args:
            filename: Name of the file to load

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
            logger.error(f"Error loading {filename}: {str(e)}", exc_info=True)
            return None

    def save_selections(self):
        """Save selected files to JSON file"""
        if not self.project_path.exists():
            return

        # Create data structure with project path and selected files
        data = {
            "project": str(self.project_path),
            "selections": [str(path) for path in self.selected_file_paths],
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
                logger.error(
                    f"Error restoring selection for {path_str}: {str(e)}", exc_info=True
                )

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
