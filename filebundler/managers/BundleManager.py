# filebundler/managers/BundleManager.py
import re
import json
import logging

from pathlib import Path
from typing import Any, List, Optional
from pydantic import ConfigDict, field_serializer

from filebundler.models.Bundle import Bundle
from filebundler.ui.notification import show_temp_notification
from filebundler.utils import (
    generate_file_bundle,
    json_dump,
    BaseModel,
)

logger = logging.getLogger(__name__)


class BundleManager(BaseModel):
    """
    Manages the creation, loading, saving, and deletion of bundles.
    """

    model_config = ConfigDict(arbitrary_types_allowed=True)
    project_path: Optional[Path] = None
    bundles: List[Bundle] = []
    bundle_content: Optional[str] = None

    @field_serializer("project_path")
    def serialize_project_path(project_path):
        return project_path.as_posix() if project_path else None

    def set_project_path(self, project_path: Path):
        """Set the project path and reset bundles"""
        self.project_path = project_path
        self.bundles = []
        self.load_bundles()

    def create_bundle(self, selected_files: List[Path]):
        """Create a bundle from selected files"""
        if not selected_files:
            return "No files selected. Please select files to bundle."

        relative_paths = [
            file_path.relative_to(self.project_path) for file_path in selected_files
        ]

        self.bundle_content = generate_file_bundle(relative_paths)

        return self.bundle_content

    def save_bundle(self, bundle_name: str, selected_files: List[Path]):
        """Save current selection as a named bundle"""
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
        file_paths = [item.relative_to(self.project_path) for item in selected_files]
        new_bundle = Bundle(name=bundle_name, file_paths=file_paths)
        self.bundles.append(new_bundle)

        # Save bundles to file
        self.save_bundles_to_disk()

        return f"Bundle '{bundle_name}' saved with {len(file_paths)} files."

    def _find_bundle_by_name(self, bundle_name: str):
        """Find a saved bundle by name"""
        for b in self.bundles:
            if b.name == bundle_name:
                return b

        return

    def create_bundle_from_saved(self, bundle_name: str):
        """Create a bundle from a saved bundle without loading it"""
        bundle = self._find_bundle_by_name(bundle_name)

        if not bundle:
            return f"Bundle '{bundle_name}' not found."

        self.bundle_content = generate_file_bundle(bundle.file_paths)

        return self.bundle_content

    def delete_bundle(self, bundle_name: str):
        """Delete a saved bundle"""
        for i, bundle in enumerate(self.bundles):
            if bundle.name == bundle_name:
                self.bundles.pop(i)
                self.save_bundles_to_disk()
                return f"Bundle '{bundle_name}' has been deleted."

        return f"Bundle '{bundle_name}' not found."

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

        return bundle_dir / "bundles.json"

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
            data = [bundle.model_dump() for bundle in self.bundles]

            # Save to file
            self._persist_to_bundles_file(data)

        except Exception as e:
            logger.error(f"Error saving bundles: {e}", exc_info=True)
            show_temp_notification(f"Error saving bundles: {str(e)}", type="error")

    def load_bundles(self):
        """Load bundles from file"""
        bundles_file = self._get_bundles_file()

        try:
            # Read from file
            with open(bundles_file, "r") as f:
                data = json.load(f)

            # Convert to Bundle objects
            self.bundles = [Bundle.model_validate(item) for item in data]
            logger.info(f"Loaded {len(self.bundles)} bundles from {bundles_file}")

        except Exception as e:
            logger.error(f"Error loading bundles: {e}", exc_info=True)
            show_temp_notification(f"Error loading bundles: {str(e)}", type="error")
