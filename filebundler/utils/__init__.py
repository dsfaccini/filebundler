# filebundler/utils/__init__.py
import io
import json
import logging
import fnmatch

from pathlib import Path
from typing import Any, List
from pydantic import BaseModel  # noqa: F401


logger = logging.getLogger(__name__)


def json_dump(data: Any, f: io.TextIOWrapper):
    json.dump(data, f, indent=4)


def ignore_patterns(relative_path: Path, ignore_patterns: List[str]):
    """Check if file matches any ignore patterns"""
    return any(
        fnmatch.fnmatch(str(relative_path), pattern) for pattern in ignore_patterns
    )


def sort_files(files: List[Path]):
    """Sort files alphabetically"""
    return sorted(files, key=lambda p: (not p.is_dir(), p.name.lower()))


def read_file(file_path: Path):
    assert file_path.exists(), f"Can't read file {file_path} because it doesn't exist"

    try:
        return file_path.read_text(encoding="utf-8", errors="replace")
    except UnicodeDecodeError as e:
        logger.error(f"UnicodeDecodeError for {file_path.name}: {e}")
        return f"Could not read {file_path.name} as text. It may be a binary file."


def ignore_directory_patterns(path: Path, ignored_patterns: List[str]):
    """
    Returns a list of all non-ignored folders, subfolders, and files in the given path.

    Args:
        path (str): The root directory path to scan
        ignored_patterns (List[str]): List of glob-style patterns to ignore (e.g., ['*.txt', '*.git/*'])

    Returns:
        List[str]: List of relative paths to non-ignored directories and files

    Raises:
        AssertionError: If the path is not a directory
    """
    # Convert string path to Path object and assert it's a directory
    root_path = Path(path)
    assert root_path.is_dir(), f"'{path}' must be a directory"

    result = []

    for item in root_path.rglob("*"):
        rel_path = item.relative_to(root_path)

        is_ignored = ignore_patterns(rel_path, ignored_patterns)

        if is_ignored:
            continue

        if item.is_file():
            result.append(rel_path)

    # Process directories - only include those that have non-ignored content
    final_result = []
    for item in result:
        final_result.append(item)
        # Add all parent directories of included files
        parent = Path(item).parent
        while parent != Path("."):
            parent_str = str(parent)
            if parent_str not in final_result:
                final_result.append(parent_str)
            parent = parent.parent

    return sort_files(final_result)
