# filebundler/models/ProjectSettings.py

from typing import List

from filebundler.utils import BaseModel
from filebundler.constants import DEFAULT_IGNORE_PATTERNS, DEFAULT_MAX_RENDER_FILES


class ProjectSettings(BaseModel):
    ignore_patterns: List[str] = DEFAULT_IGNORE_PATTERNS
    max_files: int = DEFAULT_MAX_RENDER_FILES
