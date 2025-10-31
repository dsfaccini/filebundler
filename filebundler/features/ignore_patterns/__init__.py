import shutil

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
    if relative_path.endswith("/"):
        return False

    # Check for explicit exclusion patterns (starting with !)
    for pattern in include_patterns:
        if pattern.startswith("!"):
            exclude_pattern = pattern[1:]
            # Handle directory patterns with /
            if exclude_pattern.endswith("/"):
                dir_pattern = exclude_pattern.rstrip("/")
                # Match both the directory itself and files inside
                if relative_path == dir_pattern or relative_path.startswith(exclude_pattern):
                    return False
            elif Path(relative_path).match(exclude_pattern):
                return False

    # Check for inclusion patterns
    for pattern in include_patterns:
        if not pattern.startswith("!"):
            # Handle directory patterns ending with /
            if pattern.endswith("/"):
                dir_pattern = pattern.rstrip("/")
                # Match both the directory itself and files inside
                if relative_path == dir_pattern or relative_path.startswith(pattern):
                    return True
            # Handle glob patterns
            elif Path(relative_path).match(pattern):
                return True

    # If no patterns match, exclude the file
    return False