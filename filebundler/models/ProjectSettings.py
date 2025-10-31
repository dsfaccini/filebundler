# filebundler/models/ProjectSettings.py
from typing import List, Optional, Union
from pathlib import Path

from pydantic import field_serializer, field_validator

from filebundler.utils import BaseModel
from filebundler.constants import DEFAULT_MAX_RENDER_FILES


class AutoBundleSettings(BaseModel):
    """Settings for the Auto-Bundle feature."""

    auto_refresh_project_structure: bool = True
    auto_include_bundle_files: bool = False
    user_prompt: str = "Given the TODOs in the project, select the files that are relevant to the tasks."


class ProjectSettings(BaseModel):
    include_patterns: List[str] = []
    max_files: int = DEFAULT_MAX_RENDER_FILES
    sort_files_first: bool = True
    # alphabetical_sort: Literal["asc", "desc"] = "asc"
    auto_bundle_settings: AutoBundleSettings = AutoBundleSettings()
    # NOTE the Optional is for backweard compatibility. From now on it will be always set.
    absolute_project_path: Optional[Path] = None

    @field_serializer("absolute_project_path")
    def serialize_absolute_project_path(self, value: Optional[Path]) -> Optional[str]:
        """Serialize path to POSIX format for cross-platform compatibility"""
        return value.as_posix() if value else None

    @field_validator("absolute_project_path", mode="before")
    @classmethod
    def validate_absolute_project_path(cls, value: Union[str, Path, None]) -> Optional[Path]:
        """Convert string paths to Path objects"""
        if value is None or value == "":
            return None
        return Path(value)


__all__ = ["ProjectSettings"]
