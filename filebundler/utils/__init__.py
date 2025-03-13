# filebundler/utils/__init__.py
import io
import json
import logging

from typing import Any, Dict
from pydantic import BaseModel  # noqa: F401

logger = logging.getLogger(__name__)


def json_dump(data: Dict[str, Any], f: io.BytesIO):
    json.dump(data, f, indent=4)


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


def make_file_section(relative_path: str, file_content: str):
    return f"""----- ./{relative_path} -----
{file_content}
----- END -----
"""
