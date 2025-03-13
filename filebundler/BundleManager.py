# filebundler/BundleManager.py
import re
import json
import logging
from pathlib import Path
from typing import Dict, List, Optional, Set

from filebundler.utils import json_dump, show_temp_notification

logger = logging.getLogger(__name__)


class Bundle:
    def __init__(self, name: str, file_paths: List[str]):
        self.name = name
        self.file_paths = file_paths


class BundleManager:
    """
    Manages the creation, loading, saving, and deletion of bundles.
    """

    def __init__(self, project_path: Path = Path()):
        self.project_path = project_path
        self.bundles: List[Bundle] = []
        self.bundle_content: Optional[str] = None

    def set_project_path(self, project_path: Path):
        """Set the project path and reset bundles"""
        self.project_path = project_path
        self.bundles = []
        self.load_bundles()

    def create_bundle(self, selected_files: List[Path], get_relative_path) -> str:
        """Create a bundle from selected files"""
        if not selected_files:
            return "No files selected. Please select files to bundle."

        bundle_content = []

        for file_path in selected_files:
            try:
                relative_path = get_relative_path(file_path)

                # Check if file exists
                if not file_path.exists():
                    logger.warning(f"File does not exist: {relative_path}")
                    return f"The file {relative_path} does not exist or cannot be accessed."

                # Read file content
                try:
                    file_content = file_path.read_text(
                        encoding="utf-8", errors="replace"
                    )
                except UnicodeDecodeError as e:
                    logger.error(f"UnicodeDecodeError for {file_path.name}: {e}")
                    return f"Could not read {file_path.name} as text. It may be a binary file."

                # Format with the new style
                section = [
                    f"----- ./{relative_path} -----",
                    file_content,
                    "----- END -----",
                    "",  # Empty line between files
                ]
                bundle_content.append("\n".join(section))

            except Exception as e:
                logger.error(f"Failed to read {file_path.name}: {e}", exc_info=True)
                return f"Failed to read {file_path.name}: {str(e)}"

        # Join all content
        full_bundle = "\n".join(bundle_content)
        self.bundle_content = full_bundle

        return full_bundle

    def save_bundle(
        self, bundle_name: str, selected_files: List[Path], get_relative_path
    ) -> str:
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
        file_paths = [get_relative_path(item) for item in selected_files]
        new_bundle = Bundle(bundle_name, file_paths)
        self.bundles.append(new_bundle)

        # Save bundles to file
        self.save_bundles_to_disk()

        return f"Bundle '{bundle_name}' saved with {len(file_paths)} files."

    def load_bundle(self, bundle_name: str) -> tuple[str, List[str]]:
        """
        Find a saved bundle by name

        Returns:
            tuple: (message, list of file paths in the bundle)
        """
        # Find the bundle
        bundle = None
        for b in self.bundles:
            if b.name == bundle_name:
                bundle = b
                break

        if not bundle:
            return (f"Bundle '{bundle_name}' not found.", [])

        return (
            f"Found bundle '{bundle_name}' with {len(bundle.file_paths)} files.",
            bundle.file_paths,
        )

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

        # Create bundle content
        bundle_content = []

        for rel_path in bundle.file_paths:
            try:
                full_path = self.project_path / rel_path

                # Check if file exists
                if not full_path.exists():
                    logger.warning(f"File does not exist: {rel_path}")
                    return f"The file {rel_path} does not exist or cannot be accessed."

                # Read file content
                try:
                    file_content = full_path.read_text(
                        encoding="utf-8", errors="replace"
                    )
                except UnicodeDecodeError as e:
                    logger.error(f"UnicodeDecodeError for {full_path.name}: {e}")
                    return f"Could not read {full_path.name} as text. It may be a binary file."

                # Format with the style
                section = [
                    f"----- ./{rel_path} -----",
                    file_content,
                    "----- END -----",
                    "",  # Empty line between files
                ]
                bundle_content.append("\n".join(section))

            except Exception as e:
                logger.error(f"Failed to read {rel_path}: {e}", exc_info=True)
                return f"Failed to read {rel_path}: {str(e)}"

        # Join all content
        full_bundle = "\n".join(bundle_content)
        self.bundle_content = full_bundle

        return full_bundle

    def delete_bundle(self, bundle_name: str) -> str:
        """Delete a saved bundle"""
        for i, bundle in enumerate(self.bundles):
            if bundle.name == bundle_name:
                self.bundles.pop(i)
                self.save_bundles_to_disk()
                return f"Bundle '{bundle_name}' has been deleted."

        return f"Bundle '{bundle_name}' not found."

    def rename_bundle(self, old_name: str, new_name: str) -> str:
        """Rename a saved bundle"""
        # Find the bundle
        for bundle in self.bundles:
            if bundle.name == old_name:
                bundle.name = new_name
                self.save_bundles_to_disk()
                return f"Bundle '{old_name}' renamed to '{new_name}'."

        return f"Bundle '{old_name}' not found."

    def save_bundles_to_disk(self):
        """Save bundles to file"""
        try:
            # Create .filebundler directory if it doesn't exist
            bundle_dir = self.project_path / ".filebundler"
            bundle_dir.mkdir(exist_ok=True)

            bundles_file = bundle_dir / "bundles.json"

            # Convert bundles to dictionary
            data = [
                {"name": bundle.name, "file_paths": bundle.file_paths}
                for bundle in self.bundles
            ]

            # Save to file
            with open(bundles_file, "w") as f:
                json_dump(data, f)

            logger.info(f"Saved {len(self.bundles)} bundles to {bundles_file}")

        except Exception as e:
            logger.error(f"Error saving bundles: {e}", exc_info=True)
            show_temp_notification(f"Error saving bundles: {str(e)}", type="error")

    def load_bundles(self):
        """Load bundles from file"""
        bundle_dir = self.project_path / ".filebundler"
        bundles_file = bundle_dir / "bundles.json"

        if not bundles_file.exists():
            logger.info(f"No bundles file found at {bundles_file}")
            return

        try:
            # Read from file
            with open(bundles_file, "r") as f:
                data = json.load(f)

            # Convert to Bundle objects
            self.bundles = [Bundle(item["name"], item["file_paths"]) for item in data]
            logger.info(f"Loaded {len(self.bundles)} bundles from {bundles_file}")

        except Exception as e:
            logger.error(f"Error loading bundles: {e}", exc_info=True)
            show_temp_notification(f"Error loading bundles: {str(e)}", type="error")
