# filebundler/models/FileItem.py
from pathlib import Path
from typing_extensions import List, Optional, Self
from pydantic import Field, field_serializer, model_validator

from filebundler.services.cached_operations import get_file_content, get_file_tokens
from filebundler.utils import BaseModel


class FileItem(BaseModel):
    path: Path
    project_path: Path
    parent: Optional["FileItem"] = Field(None, exclude=True)
    children: List["FileItem"] = Field([], exclude=True, repr=False)  # type: ignore
    selected: bool = Field(False, exclude=True)

    # NOTE: activate to debug unexpected selections or deselections
    # def __setattr__(self, name, value):
    #     import logging
    #     if name == "selected":
    #         logging.warning(
    #             f"Reassigning 'selected' to {value} for FileItem: {self.path}",
    #             stack_info=True,
    #         )
    #     super().__setattr__(name, value)

    @model_validator(mode="after")
    def validate_file_item(self) -> Self:
        self.path = (self.project_path / self.path).resolve()
        return self

    @field_serializer("path")
    def serialize_path(self, path: Path) -> str:
        return self.relative.as_posix()

    @field_serializer("project_path")
    def serialize_project_path(self, project_path: Path) -> str:
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
            mtime = self.path.stat().st_mtime
            return get_file_content(str(self.path), mtime)

    @property
    def tokens(self):
        if self.path.is_file():
            mtime = self.path.stat().st_mtime
            return get_file_tokens(str(self.path), mtime)
        else:
            return sum(fi.tokens for fi in self.children)  # type: ignore

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

    def __hash__(self):
        return hash(self.path.resolve().as_posix())

    def __str__(self):
        return self.relative.as_posix()
