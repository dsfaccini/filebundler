# filebundler/models/Bundle.py
from typing import List
from pydantic import ConfigDict, field_serializer

from filebundler.utils import BaseModel


class Bundle(BaseModel):
    # model_config = ConfigDict(arbitrary_types_allowed=True)

    name: str
    file_paths: List[str]

    # @field_serializer("file_paths")
    # def serialize_file_paths(filepaths):
    #     return [p.as_posix() for p in filepaths]
