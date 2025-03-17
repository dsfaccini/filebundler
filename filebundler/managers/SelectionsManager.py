# filebundler/managers/SelectionsManager.py
import json
import logging

from pathlib import Path
from dataclasses import dataclass
from typing import Any, Optional, List

from pydantic import ConfigDict, field_serializer

from filebundler.models.FileItem import FileItem
from filebundler.models.AppProtocol import AppProtocol

from filebundler.utils import json_dump, read_file, BaseModel
from filebundler.ui.notification import show_temp_notification

logger = logging.getLogger(__name__)


class SavedSelection(BaseModel):
    model_config = ConfigDict(extra="forbid")
    project: Path
    selections: List[Path]

    @field_serializer("project")
    def serialize_project(self, project: Path):
        return project.resolve().as_posix()


@dataclass
class SelectionsManager:
    """
    Manages the state of selected files and file selections persistence
    """

    app: AppProtocol
    selected_file: Optional[Path] = None

    @property
    def project_path(self):
        return self.app.project_path

    @property
    def file_items(self):
        return self.app.file_items

    @property
    def nr_of_selected_files(self):
        """Return the number of selected files"""
        return len(self.selected_file_items)

    @property
    def selected_file_items(self):
        """Return the selected file items - ONLY FILES"""
        return [v for v in self.app.file_items.values() if v.selected and not v.is_dir]

    @property
    def selected_file_content(self):
        """Return the contents of the selected files"""
        if not self.selected_file:
            return None
        return read_file(self.selected_file)

    @property
    def selections_file(self):
        """Get the path to the bundles file"""
        if not self.app.project_path:
            raise ValueError("No project path set, cannot save bundles")

        selections_dir = self.app.project_path / ".filebundler"
        selections_dir.mkdir(exist_ok=True)
        selections_file = selections_dir / "selections.json"
        return selections_file

    def _persist_to_selections_file(self, data: Any):
        with open(self.selections_file, "w") as f:
            json_dump(data, f)

        logger.info(f"Saved {len(data)} selections to {self.selections_file}")

    def _load_json_data(self, filename: str):
        if not self.selections_file.exists():
            logger.warning(f"{self.selections_file = } does not exist")
            return
        try:
            with open(self.selections_file, "r") as f:
                return json.load(f)
        except Exception as e:
            show_temp_notification(f"Error loading {filename}: {str(e)}", type="error")
            logger.error(f"Error loading {filename}: {str(e)}", exc_info=True)
            return None

    def save_selections(self):
        """Save selected files to JSON file"""
        data = [file_item.model_dump() for file_item in self.selected_file_items]

        self._persist_to_selections_file(data)

    def load_selections(self):
        """Load selected files from JSON file"""
        logger.info(f"Loading selections for {self.app.project_path}")

        selections_array = self._load_json_data("selections.json")
        if not selections_array:
            return

        selected_file_items = [
            FileItem.model_validate(item) for item in selections_array
        ]

        # Set selections
        for select_file_item in selected_file_items:
            file_item = self.app.file_items.get(select_file_item.path)
            if file_item:
                file_item.selected = True
            else:
                logger.warning(f"Error restoring selection for {select_file_item.path}")
                show_temp_notification(
                    f"Couldn't find '{select_file_item.relative}' in this project",
                    type="warning",
                )

    def select_all_files(self):
        """Select all files in the project"""

        for file_item in self.app.file_items.values():
            # TODO we need to handle the cases when a dir is marked as selected, it should actually just mark its children
            if not file_item.is_dir:
                file_item.selected = True

        self.save_selections()

        logger.info(f"Selected all {self.nr_of_selected_files} files")
        show_temp_notification(
            f"Selected all {self.nr_of_selected_files} files", type="success"
        )

    def clear_all_selections(self):
        """Clear all selected files"""
        try:
            # for path, file_item in self.app.file_items.items():
            #     if not file_item.is_dir:
            #         file_item.selected = False

            nr_of_selected_files = self.nr_of_selected_files

            for file_item in self.app.file_items.values():
                file_item.selected = False

            self.save_selections()
            self.app.bundles.current_bundle = None

            logger.info(f"Unselected all {nr_of_selected_files} files")
            show_temp_notification(
                f"Unselected all {len(self.app.file_items)} files", type="success"
            )
        except Exception as e:
            logger.error(f"Error unselecting all files: {e}", exc_info=True)
            show_temp_notification(
                f"Error unselecting all files: {str(e)}", type="error"
            )
