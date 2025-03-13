# filebundler/Bundle.py
from typing import List


class Bundle:
    def __init__(self, name: str, file_paths: List[str]):
        self.name = name
        self.file_paths = file_paths
