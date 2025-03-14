# filebundler/models/FileItem.py

from pathlib import Path


class FileItem:
    def __init__(self, path: Path):
        self.path = path
        self.name = path.name
        self.children = []
        self.selected = False

    @property
    def is_dir(self):
        return self.path.is_dir()

    @property
    def parent(self):
        return FileItem(self.path.parent)

    def __repr__(self):
        return f"FileItem({self.path}, is_dir={self.is_dir})"
