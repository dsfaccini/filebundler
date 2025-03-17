# filebundler/models/AppProtocol.py
from typing import Dict
from pathlib import Path
from dataclasses import dataclass

from filebundler.models.FileItem import FileItem
from filebundler.managers.BundleManager import BundleManager


@dataclass
class AppProtocol:
    project_path: Path
    file_items: Dict[Path, FileItem]
    bundles: BundleManager
