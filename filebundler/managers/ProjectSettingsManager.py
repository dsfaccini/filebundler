# filebundler/managers/ProjectSettingsManager.py
import logging

from pathlib import Path

from filebundler.utils import json_dump, read_file
from filebundler.models.ProjectSettings import ProjectSettings


class ProjectSettingsManager:
    def __init__(self, project_path: Path):
        self.project_path = project_path
        self.project_settings = ProjectSettings()
        self.settings_dir = self.project_path / ".filebundler"
        self.settings_dir.mkdir(exist_ok=True)
        self.settings_file = self.settings_dir / "settings.json"

    def load_project_settings(self):
        if not self.settings_file.exists():
            self.save_project_settings()
            return self.project_settings

        try:
            json_text = read_file(self.settings_file)
            self.project_settings = ProjectSettings.model_validate_json(json_text)
        except Exception as e:
            logging.error(
                f"Error loading project settings from {self.settings_file}: {str(e)}"
            )

        return self.project_settings

    def save_project_settings(self):
        try:
            with open(self.settings_file, "w") as f:
                json_dump(self.project_settings.model_dump(), f)

            return True
        except Exception as e:
            print(f"Error saving project settings: {str(e)}")
            return False
