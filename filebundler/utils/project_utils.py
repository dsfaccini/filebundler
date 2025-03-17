# filebundler/utils/project_utils.py
import fnmatch

from typing import List
from pathlib import Path

from filebundler.models.ProjectSettings import ProjectSettings


def sort_files(files: List[Path], ps: ProjectSettings):
    return sorted(
        files,
        key=lambda p: (p.is_file(), p.name.lower())
        if ps.files_first
        else (p.is_dir(), p.name.lower()),
    )


def ignore_patterns(relative_path: Path, ignore_patterns: List[str]):
    """Check if file matches any ignore patterns"""
    return any(
        fnmatch.fnmatch(str(relative_path), pattern) for pattern in ignore_patterns
    )
