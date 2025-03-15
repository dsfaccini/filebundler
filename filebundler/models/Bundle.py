# filebundler/models/Bundle.py
from typing import List

from filebundler.models.FileItem import FileItem
from filebundler.utils import BaseModel, read_file


class Bundle(BaseModel):
    name: str
    file_items: List[FileItem]

    @property
    def code_export(self):
        return f"""<?xml version="1.0" encoding="UTF-8"?>
<FileBundle>
    {"".join(make_file_section(file_item) for file_item in self.file_items)}
</FileBundle>
"""


def make_file_section(file_item: FileItem):
    # NOTE we could add error handling

    return f"""<File>
    <FilePath>
        {file_item}
    </FilePath>
    <FileContent>
{read_file(file_item.path)}
    </FileContent>
</File>
"""
