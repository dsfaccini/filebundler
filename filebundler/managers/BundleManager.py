# filebundler/managers/BundleManager.py
import re
import json
import logging

from pathlib import Path
from typing import Any, List, Optional
from pydantic import ConfigDict, field_serializer

from filebundler.models.Bundle import Bundle
from filebundler.models.FileItem import FileItem

from filebundler.utils import json_dump, BaseModel
from filebundler.ui.notification import show_temp_notification

logger = logging.getLogger(__name__)


class BundleManager(BaseModel):
    """
    Manages the creation, loading, saving, and deletion of bundles.
    """

    model_config = ConfigDict(arbitrary_types_allowed=True)
    project_path: Optional[Path] = None
    # TODO refactor to use a Dict[str, Bundle] instead of a List[Bundle] to avoid duplicate bundles
    # we can then remove the duplicate check in the 'save_bundle' method
    bundles: List[Bundle] = []
    current_bundle: Optional[Bundle] = None

    @field_serializer("project_path")
    def serialize_project_path(self, project_path):
        return project_path.as_posix() if project_path else None

    @property
    def nr_of_bundles(self):
        return len(self.bundle_dict)

    @property
    def bundle_dict(self):
        return {b.name: b for b in self.bundles}

    def save_bundle(self, bundle_name: str, selected_file_items: List[FileItem]):
        """Save current selection as a named bundle"""

        # Check if name is valid (lowercase alphanumeric)
        assert re.fullmatch(r"[a-z0-9-]+", bundle_name), (
            "Bundle name must be lowercase, alphanumeric, and may include hyphens."
        )

        # Check for duplicate names
        for b in self.bundles:
            if b.name == bundle_name:
                # Remove existing bundle with same name
                self.bundles = [b for b in self.bundles if b.name != bundle_name]
                break

        new_bundle = Bundle(name=bundle_name, file_items=selected_file_items)
        self.bundles.append(new_bundle)

        self.save_bundles_to_disk()

        return new_bundle

    def _persist_to_bundles_file(self, data: Any):
        """Persist data to bundles file"""
        bundles_file = self._get_bundles_file()

        # Save to file
        with open(bundles_file, "w") as f:
            json_dump(data, f)

        logger.info(f"Saved {len(data)} bundles to {bundles_file}")

    def save_bundles_to_disk(self):
        """Save bundles to file"""
        try:
            # Convert bundles to dictionary
            for bundle in self.bundles:
                for file_item in bundle.file_items:
                    if not file_item.path.exists():
                        bundle.file_items.remove(file_item)
                        show_temp_notification(
                            f"Removed '{file_item.relative}' from bundle because it was not found.",
                            type="warning",
                        )
            data = [bundle.model_dump() for bundle in self.bundles]

            self._persist_to_bundles_file(data)

        except Exception as e:
            logger.error(f"Error saving bundles: {e}", exc_info=True)
            show_temp_notification(f"Error saving bundles: {str(e)}", type="error")

    def _find_bundle_by_name(self, bundle_name: str):
        """Find a saved bundle by name"""
        for b in self.bundles:
            if b.name == bundle_name:
                return b

        return

    def delete_bundle(self, bundle_name: str):
        """Delete a saved bundle"""
        for i, bundle in enumerate(self.bundles):
            if bundle.name == bundle_name:
                self.bundles.pop(i)
                logger.info(f"Deleted bundle '{bundle_name}'.")
                self.save_bundles_to_disk()
        else:
            logger.warning(f"No bundle found with {bundle_name = }.")

    def rename_bundle(self, old_name: str, new_name: str):
        """Rename a saved bundle"""
        # Find the bundle
        for bundle in self.bundles:
            if bundle.name == old_name:
                bundle.name = new_name
                self.save_bundles_to_disk()
                return f"Bundle '{old_name}' renamed to '{new_name}'."

        return f"Bundle '{old_name}' not found."

    def _get_bundles_file(self):
        """Get the path to the bundles file"""
        if not self.project_path:
            raise ValueError("No project path set, cannot save bundles")

        bundle_dir = self.project_path / ".filebundler"
        bundle_dir.mkdir(exist_ok=True)
        bundles_file = bundle_dir / "bundles.json"
        return bundles_file

    def load_bundles(self, project_path: Path):
        """Load bundles from file"""
        self.project_path = project_path
        bundles_file = self._get_bundles_file()

        if bundles_file.exists():
            try:
                # Read from file
                with open(bundles_file, "r") as f:
                    data = json.load(f)

                # Convert to Bundle objects
                for item in data:
                    bundle = Bundle.model_validate(item)
                    for file_item in bundle.file_items:
                        if not file_item.path.exists():
                            logger.warning(f"File not found: {file_item.path}")
                            show_temp_notification(
                                f"File '{file_item.relative}' was not found",
                                type="error",
                            )
                            bundle.file_items.remove(file_item)

                        self.bundles.append(bundle)
                # NOTE this will not persist the removal, unless the user manually saves the bundle again
                logger.info(f"Loaded {len(self.bundles)} bundles from {bundles_file}")
            except Exception as e:
                logger.error(f"Error loading bundles: {e}", exc_info=True)
                show_temp_notification(f"Error loading bundles: {str(e)}", type="error")
