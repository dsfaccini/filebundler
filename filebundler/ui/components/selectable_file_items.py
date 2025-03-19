# filebundler/ui/components.py/selectable_file_items.py
import logfire
import streamlit as st

from pathlib import Path
from typing import List

from filebundler.FileBundlerApp import FileBundlerApp
from filebundler.models.FileItem import FileItem


def render_selectable_file_items_list(
    app: FileBundlerApp,
    key_prefix: str,
    from_paths: List[Path] = [],
    from_items: List[FileItem] = [],
):
    if from_paths:
        file_items: List[FileItem] = []
        for file_path in from_paths:
            file_item = app.file_items.get(file_path)
            if file_item:
                file_items.append(file_item)
            else:
                logfire.warning(
                    f"the following file doesn't exist in the app: {file_path}"
                )
                continue
    else:
        file_items = from_items

    for file_item in file_items:
        st.checkbox(
            label=str(file_item.relative),
            key=f"{key_prefix}_select_{file_item.path}",
            value=file_item.selected,
        )
