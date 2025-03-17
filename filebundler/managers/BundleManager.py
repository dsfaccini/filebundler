# filebundler/managers/BundleManager.py
import logging

from pathlib import Path
from typing import Dict, Optional
from pydantic import ConfigDict, field_serializer

from filebundler.models.Bundle import Bundle

from filebundler.utils import (
    dump_model_to_file,
    BaseModel,
    load_model_from_file,
)
from filebundler.ui.notification import show_temp_notification

logger = logging.getLogger(__name__)


class BundleManager(BaseModel):
    """
    Manages the creation, loading, saving, and deletion of bundles.
    """

    model_config = ConfigDict(arbitrary_types_allowed=True)
    project_path: Optional[Path] = None
    bundles_dict: Dict[str, Bundle] = {}
    current_bundle: Optional[Bundle] = None

    @field_serializer("project_path")
    def serialize_project_path(self, project_path):
        return project_path.as_posix() if project_path else None

    @property
    def nr_of_bundles(self):
        return len(self.bundles_dict)

    @property
    def bundles_dir(self) -> Path:
        """Get the path to the bundles directory"""
        if not self.project_path:
            raise ValueError("No project path set, cannot access bundles")

        bundle_dir = self.project_path / ".filebundler" / "bundles"
        bundle_dir.mkdir(parents=True, exist_ok=True)
        return bundle_dir

    def _get_bundle_path(self, bundle_name: str) -> Path:
        """Get the path to a specific bundle file"""
        return self.bundles_dir / f"{bundle_name}.json"

    def save_bundle(self, new_bundle: Bundle):
        if new_bundle.name in self.bundles_dict:
            del self.bundles_dict[new_bundle.name]

        self.bundles_dict[new_bundle.name] = new_bundle

        self._save_bundle_to_disk(new_bundle)
        self.activate_bundle(new_bundle)

        return new_bundle

    def _save_bundle_to_disk(self, bundle: Bundle):
        """Save a single bundle to its own file"""
        try:
            bundle.prune()

            bundle_path = self._get_bundle_path(bundle.name)
            dump_model_to_file(bundle, bundle_path)

            logger.info(f"Saved bundle '{bundle.name}' to {bundle_path}")

        except Exception as e:
            logger.error(f"Error saving bundle '{bundle.name}': {e}", exc_info=True)
            show_temp_notification(
                f"Error saving bundle '{bundle.name}': {str(e)}", type="error"
            )

    def save_bundles_to_disk(self):
        """Save all bundles to disk as individual files"""
        try:
            for bundle in self.bundles_dict.values():
                self._save_bundle_to_disk(bundle)

        except Exception as e:
            logger.error(f"Error saving bundles: {e}", exc_info=True)
            show_temp_notification(f"Error saving bundles: {str(e)}", type="error")

    def _find_bundle_by_name(self, bundle_name: str) -> Optional[Bundle]:
        """Find a saved bundle by name"""
        return self.bundles_dict.get(bundle_name)

    def delete_bundle(self, bundle_to_delete: Bundle):
        """Delete a saved bundle"""
        if not self.bundles_dict.get(bundle_to_delete.name):
            logger.warning(f"No bundle found with name '{bundle_to_delete.name}'.")
            return

        if self.current_bundle is bundle_to_delete:
            self.current_bundle = None

        del self.bundles_dict[bundle_to_delete.name]

        # Also delete the file
        bundle_path = self._get_bundle_path(bundle_to_delete.name)
        if bundle_path.exists():
            bundle_path.unlink()

        logger.info(f"Deleted bundle '{bundle_to_delete.name}'.")

    def rename_bundle(self, old_name: str, new_name: str):
        bundle = self._find_bundle_by_name(old_name)
        # Check if new name already exists
        if bundle and old_name != new_name:
            return f"Bundle with name '{new_name}' already exists."

        # Find the bundle
        if not bundle:
            return f"Bundle '{old_name}' not found."

        # Delete old file
        old_path = self._get_bundle_path(old_name)
        if old_path.exists():
            try:
                old_path.unlink()
            except Exception as e:
                logger.error(f"Error deleting old bundle file: {e}", exc_info=True)

        # Update bundle name and save
        bundle.name = new_name
        self._save_bundle_to_disk(bundle)

        return f"Bundle '{old_name}' renamed to '{new_name}'."

    def load_bundles(self, project_path: Path):
        """Load all bundles from individual files in the bundles directory"""
        self.project_path = project_path
        self.bundles_dict = {}  # Clear existing bundles

        try:
            if not self.bundles_dir.exists():
                return  # No bundles directory yet

            # Load each bundle file
            for bundle_file in self.bundles_dir.glob("*.json"):
                try:
                    bundle = load_model_from_file(Bundle, bundle_file)
                    bundle.prune()
                    self.bundles_dict[bundle.name] = bundle
                    logger.info(f"Loaded bundle '{bundle.name}' from {bundle_file}")

                except Exception as e:
                    error_msg = f"Error loading bundle from {bundle_file}: {str(e)}"
                    logger.error(error_msg, exc_info=True)
                    show_temp_notification(error_msg, type="error")

        except Exception as e:
            logger.error(f"Error loading bundles: {e}", exc_info=True)
            show_temp_notification(f"Error loading bundles: {str(e)}", type="error")

    def activate_bundle(self, bundle: Bundle):
        assert self._find_bundle_by_name(bundle.name), (
            f"Bundle '{bundle.name}' not found in bundles"
        )
        self.current_bundle = bundle
        logger.info(f"Activated bundle '{bundle.name}'")
