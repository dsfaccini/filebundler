# filebundler/managers/BundleManager.py
import re
import pdb
import json
import logging

from pathlib import Path
from typing import List, Optional
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

    @property
    def bundles_file(self):
        """Get the path to the bundles file"""
        if not self.project_path:
            raise ValueError("No project path set, cannot save bundles")

        bundle_dir = self.project_path / ".filebundler"
        bundle_dir.mkdir(exist_ok=True)
        bundles_file = bundle_dir / "bundles.json"
        return bundles_file

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
        self.activate_bundle(new_bundle)

        return new_bundle

    def remove_deleted_files_from_bundle(self, bundle: Bundle):
        """Remove files that no longer exist from a bundle"""
        for file_item in bundle.file_items:
            if not file_item.path.exists():
                logger.warning(f"File not found: {file_item.path}")
                show_temp_notification(
                    f"File '{file_item.relative}' was not found",
                    type="error",
                )
                # NOTE this will not persist the removal, unless the user manually saves the bundle again
                bundle.file_items.remove(file_item)

    def save_bundles_to_disk(self):
        """Save bundles to file"""
        try:
            for bundle in self.bundles:
                self.remove_deleted_files_from_bundle(bundle)

            data = [bundle.model_dump() for bundle in self.bundles]

            with open(self.bundles_file, "w") as f:
                json_dump(data, f)

        except Exception as e:
            logger.error(f"Error saving bundles: {e}", exc_info=True)
            show_temp_notification(f"Error saving bundles: {str(e)}", type="error")

    def _find_bundle_by_name(self, bundle_name: str):
        """Find a saved bundle by name"""
        for b in self.bundles:
            if b.name == bundle_name:
                return b

        return

    def delete_bundle(self, bundle_to_delete: Bundle):
        """Delete a saved bundle"""
        for bundle in self.bundles:
            if bundle is bundle_to_delete:
                # pdb.set_trace()
                self.bundles.remove(bundle)
                self.save_bundles_to_disk()
                logger.info(f"Deleted bundle '{bundle_to_delete.name}'.")
                break
        else:
            logger.warning(f"No bundle found with {bundle_to_delete.name = }.")

    def rename_bundle(self, old_name: str, new_name: str):
        """Rename a saved bundle"""
        # Find the bundle
        for bundle in self.bundles:
            if bundle.name == old_name:
                bundle.name = new_name
                self.save_bundles_to_disk()
                return f"Bundle '{old_name}' renamed to '{new_name}'."

        return f"Bundle '{old_name}' not found."

    def load_bundles(self, project_path: Path):
        self.project_path = project_path

        if self.bundles_file.exists():
            try:
                with open(self.bundles_file, "r") as f:
                    data = json.load(f)

                for item in data:
                    bundle = Bundle.model_validate(item)
                    self.remove_deleted_files_from_bundle(bundle)
                    self.bundles.append(bundle)

            except Exception as e:
                logger.error(f"Error loading bundles: {e}", exc_info=True)
                show_temp_notification(f"Error loading bundles: {str(e)}", type="error")

    def activate_bundle(self, bundle: Bundle):
        assert bundle in self.bundles, f"Bundle '{bundle.name}' not found in bundles"
        self.current_bundle = bundle
        logger.info(f"Activated bundle '{bundle.name}'")
