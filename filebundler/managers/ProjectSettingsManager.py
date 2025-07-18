# filebundler/managers/ProjectSettingsManager.py
import logging

from pathlib import Path
from typing import Optional

from filebundler.utils import json_dump, read_file
from filebundler.models.ProjectSettings import ProjectSettings
from filebundler.services.path_validation import validate_project_path, PathValidationResult

from filebundler.features.ignore_patterns import copy_default_ignore_patterns

logger = logging.getLogger(__name__)


class ProjectSettingsManager:
    def __init__(self, project_path: Path):
        self.project_path = project_path
        self.project_settings = ProjectSettings()
        self.filebundler_dir = self.project_path / ".filebundler"
        self.filebundler_dir.mkdir(exist_ok=True)
        self.settings_file = self.filebundler_dir / "settings.json"
        self.ignore_patterns_file = self.filebundler_dir / "ignore-patterns.txt"
        self.path_validation_result: Optional[PathValidationResult] = None
        
        if not self.ignore_patterns_file.exists():
            copy_default_ignore_patterns(self.filebundler_dir)
        
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

    def load_ignore_patterns(self):
        # Try to load from ignore-patterns.txt first
        if self.ignore_patterns_file.exists():
            try:
                content = read_file(self.ignore_patterns_file)
                patterns = [
                    line.strip() for line in content.splitlines() if line.strip()
                ]
                self.project_settings.ignore_patterns = patterns
                return patterns
            except Exception as e:
                logger.warning(f"Error reading ignore-patterns.txt: {str(e)}")

        # Fallback: try to load from settings
        if self.settings_file.exists():
            try:
                json_text = read_file(self.settings_file)
                settings = ProjectSettings.model_validate_json(json_text)
                if settings.ignore_patterns:
                    self.project_settings.ignore_patterns = settings.ignore_patterns
                    # Migrate to ignore-patterns.txt
                    self.save_ignore_patterns()
                    return settings.ignore_patterns
            except Exception as e:
                logger.warning(f"Error reading ignore patterns from settings: {str(e)}")
                
        # Fallback: try to load from .gitignore
        project_gitignore_path = self.project_path / ".gitignore"
        try:
            if project_gitignore_path.exists() and not self.ignore_patterns_file.exists():
                gitignore_content = read_file(project_gitignore_path)
                if gitignore_content:
                    ignore_patterns = [
                        line.strip()
                        for line in gitignore_content.splitlines()
                        if line.strip()
                    ]
                    self.project_settings.ignore_patterns = ignore_patterns
                    # Migrate to ignore-patterns.txt
                    self.save_ignore_patterns()
                    return ignore_patterns
        except Exception as e:
            logger.warning(
                f"Error reading .gitignore file: {str(e)}. Using default ignore patterns."
            )
        # If all else fails, use whatever is in the model (defaults)
        return self.project_settings.ignore_patterns

    def save_ignore_patterns(self):
        try:
            with open(self.ignore_patterns_file, "w", encoding="utf-8") as f:
                for pattern in self.project_settings.ignore_patterns:
                    f.write(pattern + "\n")
            logger.info(f"Ignore patterns saved to {self.ignore_patterns_file}")
            return True
        except Exception as e:
            logger.error(f"Error saving ignore patterns: {str(e)}")
            return False

    def load_project_settings(self):
        self.load_ignore_patterns()
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
        self.save_ignore_patterns()
        try:
            with open(self.settings_file, "w", encoding="utf-8") as f:
                # Save all settings, but ignore_patterns will be loaded from file and not written
                settings_dict = self.project_settings.model_dump()
                if "ignore_patterns" in settings_dict:
                    del settings_dict["ignore_patterns"]
                json_dump(settings_dict, f)
            logger.info(f"Project settings saved to {self.settings_file}")
            return True
        except Exception as e:
            logger.error(f"Error saving project settings: {str(e)}")
            return False
