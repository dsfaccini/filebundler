# filebundler/models/Bundle.py
from typing import List

from pydantic import field_validator

from filebundler.models.FileItem import FileItem
from filebundler.utils import BaseModel, read_file


class Bundle(BaseModel):
    name: str
    file_items: List[FileItem]

    @field_validator("file_items")
    def check_file_items(cls, values: List[FileItem]):
        return [fi for fi in values if fi.path.exists() and not fi.is_dir]

    # FUTURE TODO, not now: create XML with a library so it handles special characters and such
    @property
    def code_export(self):
        return f"""<?xml version="1.0" encoding="UTF-8"?>
<FileBundle>
{"\n".join(make_file_section(file_item) for file_item in self.file_items if not file_item.is_dir)}
</FileBundle>"""


def make_file_section(file_item: FileItem):
    # NOTE we could add error handling

    return f"""    <File>
        <FilePath>
        {file_item}
        </FilePath>
        <FileContent>
{read_file(file_item.path)}
        </FileContent>
    </File>"""
