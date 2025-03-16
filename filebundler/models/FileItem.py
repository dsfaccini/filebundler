# filebundler/models/FileItem.py
from pathlib import Path
from typing_extensions import List, Optional, Self
from pydantic import Field, field_serializer, model_validator

from filebundler.utils import BaseModel, read_file


class FileItem(BaseModel):
    path: Path
    project_path: Path
    parent: Optional["FileItem"] = Field(None, exclude=True)
    children: List["FileItem"] = Field([], exclude=True)
    selected: bool = Field(False, exclude=True)

    @model_validator(mode="after")
    def validate_file_item(self) -> Self:
        self.path = (self.project_path / self.path).resolve()
        return self

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
        if self.is_dir:
            for child in self.children:
                if child.is_dir and child.selected != self.selected:
                    child.toggle_selected()
                else:
                    child.selected = self.selected
        else:
            if self.parent:
                self.parent.selected = all(
                    [child.selected for child in self.parent.children]
                )

    def __str__(self):
        return self.relative.as_posix()
