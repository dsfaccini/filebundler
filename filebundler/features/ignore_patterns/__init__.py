import shutil
import fnmatch

from typing import List
from pathlib import Path


EXAMPLE_INCLUDE_FILE = Path(__file__).parent / "default-include-patterns.txt"


def copy_default_include_patterns(filebundler_dir: Path):
    include_patterns_file = filebundler_dir / ".include"
    if not include_patterns_file.exists():
        shutil.copy(EXAMPLE_INCLUDE_FILE, include_patterns_file)


def should_include_path(relative_path: str, include_patterns: List[str]):
    """Check if file matches any include patterns"""
    # If no include patterns are specified, include everything
    if not include_patterns:
        return True

    # Special case: if the path is just a directory (ends with /), exclude it
    # unless it's explicitly matched by a non-directory pattern
    if relative_path.endswith("/"):
        return False

    # Normalize patterns to handle directory patterns (ending with /)
    normalized_patterns: List[str] = []
    for pattern in include_patterns:
        if pattern.endswith("/"):
            # Convert directory patterns like "dir/" to "dir/**/*" and "dir/*"
            # This allows matching files and subdirectories within the directory
            normalized_patterns.append(f"{pattern}**/*")
            normalized_patterns.append(f"{pattern}*")
        else:
            normalized_patterns.append(pattern)

    # Check for explicit exclusion patterns (starting with !)
    for pattern in normalized_patterns:
        if pattern.startswith("!"):
            exclude_pattern = pattern[1:]
            if fnmatch.fnmatch(relative_path, exclude_pattern):
                return False

    # Check for inclusion patterns
    for pattern in normalized_patterns:
        if not pattern.startswith("!") and fnmatch.fnmatch(relative_path, pattern):
            return True

    # If no patterns match, exclude the file
    return False
