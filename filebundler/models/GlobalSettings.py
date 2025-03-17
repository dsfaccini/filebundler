# filebundler/models/GlobalSettings.py
from typing import List
from pathlib import Path

from pydantic import field_serializer

from filebundler.utils import BaseModel
from filebundler.constants import DEFAULT_IGNORE_PATTERNS, DEFAULT_MAX_RENDER_FILES


class GlobalSettings(BaseModel):
    ignore_patterns: List[str] = DEFAULT_IGNORE_PATTERNS
    max_files: int = DEFAULT_MAX_RENDER_FILES
    recent_projects: List[Path] = []

    @field_serializer("recent_projects")
    def recent_projects_serializer(self, value: List[Path]):
        return [p.as_posix() for p in value]

    @property
    def recent_projects_str(self):
        return [p.as_posix() for p in self.recent_projects]
