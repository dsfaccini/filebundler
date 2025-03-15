# filebundler/models/FileItem.py
from pathlib import Path
from typing import List, Optional
from pydantic import Field, field_serializer, field_validator

from filebundler.utils import BaseModel, read_file


class FileItem(BaseModel):
    path: Path
    project_path: Path
    parent: Optional["FileItem"] = Field(None, exclude=True)
    children: List["FileItem"] = Field([], exclude=True)
    selected: bool = Field(False, exclude=True)

    @field_validator("path", mode="before")
    def validate_path(cls, path):
        return Path(path).resolve()

    @field_serializer("path")
    def serialize_path(self, path):
        return self.relative.as_posix()

    @field_serializer("project_path")
    def serialize_project_path(self, project_path):
        return project_path.resolve().as_posix()

    @property
    def relative(self):
        return self.path.relative_to(self.project_path)

    @property
    def name(self):
        return self.path.name

    @property
    def is_dir(self):
        return self.path.is_dir()

    @property
    def content(self):
        if self.path.is_file():
            return read_file(self.path)

    def toggle_selected(self):
        self.selected = not self.selected

    def __str__(self):
        return self.relative.as_posix()
