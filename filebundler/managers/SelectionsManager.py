# filebundler/managers/SelectionsManager.py
import json
import logging

from pathlib import Path
from typing import Any, Dict, Optional

from filebundler.utils import json_dump, BaseModel, read_file

from filebundler.models.FileItem import FileItem
from filebundler.ui.notification import show_temp_notification

logger = logging.getLogger(__name__)


class SelectionsManager(BaseModel):
    """
    Manages the state of selected files and file selections persistence
    """

    project_path: Path
    file_items: Dict[Path, FileItem]
    selected_file: Optional[Path] = None

    @property
    def nr_of_selected_files(self):
        """Return the number of selected files"""
        return len(self.selected_file_items)

    @property
    def selected_file_items(self):
        """Return the selected file items"""
        return [v for v in self.file_items.values() if v.selected]

    @property
    def selected_file_content(self):
        """Return the contents of the selected files"""
        if not self.selected_file:
            return None
        return read_file(self.selected_file)

    def _get_selections_file(self):
        """Get the path to the bundles file"""
        if not self.project_path:
            raise ValueError("No project path set, cannot save bundles")

        selections_dir = self.project_path / ".filebundler"
        selections_dir.mkdir(exist_ok=True)
        selections_file = selections_dir / "selections.json"
        return selections_file

    def _persist_to_selections_file(self, data: Any):
        """Persist data to bundles file"""
        selections_file = self._get_selections_file()

        # Save to file
        with open(selections_file, "w") as f:
            json_dump(data, f)

        logger.info(f"Saved {len(data)} selections to {selections_file}")

    def _load_json_data(self, filename: str):
        selections_file = self._get_selections_file()

        if selections_file.exists():
            try:
                with open(selections_file, "r") as f:
                    return json.load(f)
            except Exception as e:
                logger.error(f"Error loading {filename}: {str(e)}", exc_info=True)
                return None

    def save_selections(self):
        """Save selected files to JSON file"""
        project_path = self.project_path.resolve().as_posix()
        data = {
            "project": project_path,
            "selections": [
                file_item.model_dump() for file_item in self.selected_file_items
            ],
        }

        self._persist_to_selections_file(data)

    def load_selections(self, project_path: Path):
        """Load selected files from JSON file"""
        self.project_path = project_path

        data = self._load_json_data("selections.json")
        if not data:
            logger.warning(f"selections.json was empty for {project_path}")
            return

        # Check if the loaded data is for the current project
        if Path(data.get("project")) != str(self.project_path):
            show_temp_notification(
                f"Selections file is for a different project: {data.get('project')}",
                type="error",
            )
            return

        # Set selections
        path_strings = data.get("selections", [])
        for path_string in path_strings:
            path = Path(path_string)
            file_item = self.file_items.get(path)
            if file_item:
                file_item.selected = True
            else:
                logger.warning(f"Error restoring selection for {path_string}")
                show_temp_notification(
                    f"Error restoring selection for {path_string}", type="error"
                )

    def select_all_files(self):
        """Select all files in the project"""

        for file_item in self.file_items.values():
            if not file_item.is_dir:
                file_item.selected = True

            # Save selections
            self.save_selections()

            logger.info(f"Selected all {self.selected_file_items} files")
            show_temp_notification(
                f"Selected all {self.selected_file_items} files", type="success"
            )

    def clear_all_selections(self):
        """Clear all selected files"""
        try:
            # for path, file_item in self.file_items.items():
            #     if not file_item.is_dir:
            #         file_item.selected = False

            nr_of_selected_files = self.nr_of_selected_files

            for file_item in self.selected_file_items:
                file_item.selected = False

            self.save_selections()
            logger.info(f"Unselected all {nr_of_selected_files} files")
            show_temp_notification(
                f"Unselected all {len(self.file_items)} files", type="success"
            )
        except Exception as e:
            logger.error(f"Error unselecting all files: {e}", exc_info=True)
            show_temp_notification(
                f"Error unselecting all files: {str(e)}", type="error"
            )
