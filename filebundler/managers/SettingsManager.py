# filebundler/managers/SettingsManager.py
import json

from pathlib import Path

from filebundler.utils import json_dump
from filebundler.constants import DISPLAY_NR_OF_RECENT_PROJECTS

from filebundler.models.ProjectSettings import ProjectSettings


# TODO settings should be divided into global and project settings
class SettingsManager:
    def __init__(self):
        # Settings directory in user home
        self.settings_dir = Path.home() / ".filebundler"
        self.settings_dir.mkdir(exist_ok=True)

        # Project-level settings are stored in the project directory
        self.project_settings = ProjectSettings()

        # Recent projects file
        self.recent_projects_file = self.settings_dir / "recent_projects.json"

        # Load recent projects
        self.recent_projects = self._load_recent_projects()

    def _load_recent_projects(self):
        """Load list of recent projects"""
        if self.recent_projects_file.exists():
            try:
                with open(self.recent_projects_file, "r") as f:
                    return json.load(f)
            except Exception:
                return []
        return []

    def save_recent_projects(self):
        """Save recent projects list"""
        self.recent_projects = [p for p in self.recent_projects if p and p != "."]
        try:
            with open(self.recent_projects_file, "w") as f:
                json_dump(self.recent_projects, f)
        except Exception as e:
            print(f"Error saving recent projects: {str(e)}")

    def add_recent_project(self, project_path):
        """Add a project to recent projects list"""
        # Convert to string in case it's a Path
        project_path = str(project_path)

        # Remove this project if it already exists in the list
        if project_path in self.recent_projects:
            self.recent_projects.remove(project_path)

        # Add to the beginning of the list
        self.recent_projects.insert(0, project_path)

        # Keep only the last 5 projects
        self.recent_projects = self.recent_projects[:DISPLAY_NR_OF_RECENT_PROJECTS]

        # Save the updated list
        self.save_recent_projects()

    def get_recent_projects(self):
        """Get list of recent projects"""
        # Filter out projects that don't exist anymore
        existing_projects = [p for p in self.recent_projects if Path(p).exists()]

        # If the list changed, save it
        if len(existing_projects) != len(self.recent_projects):
            self.recent_projects = existing_projects
            self.save_recent_projects()

        return self.recent_projects

    def load_project_settings(self, project_path: str):
        """Load settings for a specific project"""
        project_path = Path(project_path)
        settings_file = project_path / ".filebundler" / "settings.json"

        if not settings_file.exists():
            return self.project_settings

        try:
            (project_path / ".filebundler").mkdir(exist_ok=True)
            self.project_settings = ProjectSettings.model_validate_json(
                settings_file.read_text()
            )
            return self.project_settings

        except Exception as e:
            print(f"Error loading project settings: {str(e)}")
            return self.project_settings

    def save_project_settings(self, project_path: str):
        """Save settings for a specific project"""
        project_path = Path(project_path)
        settings_dir = project_path / ".filebundler"
        settings_file = settings_dir / "settings.json"

        try:
            settings_dir.mkdir(exist_ok=True)
            with open(settings_file, "w") as f:
                json_dump(self.project_settings.model_dump(), f)

            return True
        except Exception as e:
            print(f"Error saving project settings: {str(e)}")
            return False
