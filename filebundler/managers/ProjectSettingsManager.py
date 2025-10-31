# filebundler/managers/ProjectSettingsManager.py
import logging

from pathlib import Path
from typing import Optional

from filebundler.utils import json_dump, read_file
from filebundler.models.ProjectSettings import ProjectSettings
from filebundler.services.path_validation import validate_project_path, PathValidationResult

from filebundler.features.ignore_patterns import copy_default_include_patterns

logger = logging.getLogger(__name__)


class ProjectSettingsManager:
    def __init__(self, project_path: Path):
        self.project_path = project_path
        self.project_settings = ProjectSettings()
        self.filebundler_dir = self.project_path / ".filebundler"
        self.filebundler_dir.mkdir(exist_ok=True)
        self.settings_file = self.filebundler_dir / "settings.json"
        self.include_patterns_file = self.filebundler_dir / ".include"
        self.path_validation_result: Optional[PathValidationResult] = None

        if not self.include_patterns_file.exists():
            copy_default_include_patterns(self.filebundler_dir)

        self.load_project_settings()
        self.save_project_settings()

    def validate_project_path(self) -> PathValidationResult:
        """
        Validate the current project path against the stored path.
        
        Returns:
            PathValidationResult with validation details
        """
        stored_path = self.project_settings.absolute_project_path
        self.path_validation_result = validate_project_path(self.project_path, stored_path)
        
        if not self.path_validation_result.is_valid:
            logger.warning(f"Project path validation failed: {self.path_validation_result.issues}")
        
        return self.path_validation_result

    def update_project_path(self, new_path: Path) -> bool:
        """
        Update the stored project path and save settings.
        
        Args:
            new_path: The new project path to store
            
        Returns:
            True if successful, False otherwise
        """
        try:
            self.project_settings.absolute_project_path = new_path.resolve()
            return self.save_project_settings()
        except Exception as e:
            logger.error(f"Error updating project path: {e}")
            return False

    def load_include_patterns(self):
        # Try to load from .include file first
        if self.include_patterns_file.exists():
            try:
                content = read_file(self.include_patterns_file)
                patterns = [
                    line.strip() for line in content.splitlines() if line.strip()
                ]
                self.project_settings.include_patterns = patterns
                return patterns
            except Exception as e:
                logger.warning(f"Error reading .include file: {str(e)}")

        # Fallback: try to load from settings (for migration)
        if self.settings_file.exists():
            try:
                json_text = read_file(self.settings_file)
                settings = ProjectSettings.model_validate_json(json_text)
                if settings.include_patterns:
                    self.project_settings.include_patterns = settings.include_patterns
                    # Migrate to .include file
                    self.save_include_patterns()
                    return settings.include_patterns
            except Exception as e:
                logger.warning(f"Error reading include patterns from settings: {str(e)}")



        # If all else fails, use whatever is in the model (defaults)
        return self.project_settings.include_patterns

    def save_include_patterns(self):
        try:
            with open(self.include_patterns_file, "w", encoding="utf-8") as f:
                for pattern in self.project_settings.include_patterns:
                    f.write(pattern + "\n")
            logger.info(f"Include patterns saved to {self.include_patterns_file}")
            return True
        except Exception as e:
            logger.error(f"Error saving include patterns: {str(e)}")
            return False

    def load_project_settings(self):
        self.load_include_patterns()
        # Always try to load other settings from settings.json
        if self.settings_file.exists():
            try:
                json_text = read_file(self.settings_file)
                loaded_settings = ProjectSettings.model_validate_json(json_text)
                # Update all fields including the new absolute_project_path
                self.project_settings.max_files = loaded_settings.max_files
                self.project_settings.sort_files_first = (
                    loaded_settings.sort_files_first
                )
                self.project_settings.auto_bundle_settings = (
                    loaded_settings.auto_bundle_settings
                )
                self.project_settings.absolute_project_path = (
                    loaded_settings.absolute_project_path
                )
            except Exception as e:
                logger.info(
                    f"Exception loading project settings from {self.settings_file}: {str(e)}"
                )

        # If no stored path, set it to current path
        if self.project_settings.absolute_project_path is None:
            self.project_settings.absolute_project_path = self.project_path.resolve()
            logger.info(f"Setting initial project path: {self.project_path}")

    def save_project_settings(self):
        self.save_include_patterns()
        try:
            with open(self.settings_file, "w", encoding="utf-8") as f:
                # Save all settings, but include_patterns will be loaded from file and not written
                settings_dict = self.project_settings.model_dump()
                if "include_patterns" in settings_dict:
                    del settings_dict["include_patterns"]
                json_dump(settings_dict, f)
            logger.info(f"Project settings saved to {self.settings_file}")
            return True
        except Exception as e:
            logger.error(f"Error saving project settings: {str(e)}")
            return False
