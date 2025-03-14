# filebundler/managers/SelectionsManager.py
import logging

from pathlib import Path
from typing import Dict, List, Set

logger = logging.getLogger(__name__)


class SelectionsManager:
    """
    Manages the state of selected files
    """

    def __init__(self):
        self.selected_file_paths: Set[Path] = set()
        self.file_items: Dict = {}

    def set_file_items(self, file_items: Dict):
        """Set the file items dictionary"""
        self.file_items = file_items

    def toggle_file_selection(self, file_path: Path):
        """Toggle selection of a file"""
        try:
            if file_path in self.selected_file_paths:
                self.selected_file_paths.remove(file_path)
                logger.info(f"Unselected file: {file_path}")
            else:
                self.selected_file_paths.add(file_path)
                logger.info(f"Selected file: {file_path}")
        except Exception as e:
            logger.error(f"Error toggling file selection: {e}", exc_info=True)

    def select_all_files(self):
        """Select all files in the project"""
        try:
            selected_count = 0

            # Recursive function to gather all file paths
            def gather_files(directory_item):
                nonlocal selected_count
                file_paths = []

                for child in directory_item.children:
                    if child.is_dir:
                        file_paths.extend(gather_files(child))
                    else:
                        file_paths.append(child.path)
                        selected_count += 1

                return file_paths

            # Get all files from the root directory
            if self.file_items:
                root_key = next(iter(self.file_items))
                root_item = self.file_items[root_key]
                all_files = gather_files(root_item)

                # Update selected files
                self.selected_file_paths = set(all_files)
                logger.info(f"Selected all {selected_count} files")
            else:
                logger.warning("No file items available to select")

        except Exception as e:
            logger.error(f"Error selecting all files: {e}", exc_info=True)

    def unselect_all_files(self):
        """Unselect all files"""
        try:
            count = len(self.selected_file_paths)
            self.selected_file_paths.clear()
            logger.info(f"Unselected all {count} files")
        except Exception as e:
            logger.error(f"Error unselecting all files: {e}", exc_info=True)

    def get_selected_files(self) -> List[Path]:
        """Get list of selected files"""
        return list(self.selected_file_paths)
