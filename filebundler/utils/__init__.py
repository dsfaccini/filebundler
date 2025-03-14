# filebundler/utils/__init__.py
import io
import json
import logging
import fnmatch

from typing import Any, Dict, List
from pathlib import Path
from pydantic import BaseModel  # noqa: F401

logger = logging.getLogger(__name__)


def json_dump(data: Dict[str, Any], f: io.BytesIO):
    json.dump(data, f, indent=4)


def ignore_patterns(relative_path: Path, ignore_patterns: List[str]):
    """Check if file matches any ignore patterns"""
    return any(
        fnmatch.fnmatch(str(relative_path), pattern) for pattern in ignore_patterns
    )


def sort_files(files: List[Path]):
    """Sort files alphabetically"""
    return sorted(files, key=lambda p: (not p.is_dir(), p.name.lower()))


def read_file(file_path: str):
    if not file_path.exists():
        logger.warning(f"File does not exist: {file_path}")
        return f"The file {file_path} does not exist or cannot be accessed."

    # Read file content
    try:
        return file_path.read_text(encoding="utf-8", errors="replace")
    except UnicodeDecodeError as e:
        logger.error(f"UnicodeDecodeError for {file_path.name}: {e}")
        return f"Could not read {file_path.name} as text. It may be a binary file."


def generate_file_bundle(relative_paths: List[Path]):
    return f"""<?xml version="1.0" encoding="UTF-8"?>
<FileBundle>
    {"".join(make_file_section(p) for p in relative_paths)}
</FileBundle>
"""


def make_file_section(relative_path: Path):
    # except Exception as e:
    # logger.error(f"Failed to read {file_path.name}: {e}", exc_info=True)
    # return f"Failed to read {file_path.name}: {str(e)}"

    return f"""<File>
    <FilePath>
        {relative_path.as_posix()}
    </FilePath>
    <FileContent>
{read_file(relative_path)}
    </FileContent>
</File>
"""
