# filebundler/models/Bundle.py
import re
import logging

from datetime import datetime
from typing import List, Optional

from pydantic import field_validator, Field, computed_field

from filebundler.models.FileItem import FileItem
from filebundler.models.BundleMetadata import (
    BundleMetadata,
    format_datetime,
    format_file_size,
)
from filebundler.services.token_count import compute_word_count
from filebundler.ui.notification import show_temp_notification
from filebundler.utils import BaseModel, read_file

logger = logging.getLogger(__name__)


class Bundle(BaseModel):
    name: str
    file_items: List[FileItem]
    metadata: BundleMetadata = Field(default_factory=BundleMetadata)

    @field_validator("name")
    def check_name(cls, value: str):
        assert re.fullmatch(r"[a-z0-9-]+", value), (
            "Bundle name must be lowercase, alphanumeric, and may include hyphens."
        )
        return value

    @field_validator("file_items")
    def check_file_items(cls, values: List[FileItem]):
        return [fi for fi in values if fi.path.exists() and not fi.is_dir]

    @computed_field  # type: ignore[prop-decorator]
    @property
    def last_modified_date(self) -> Optional[datetime]:
        """Get the most recent modification date of any file in the bundle"""
        return max(
            datetime.fromtimestamp(fi.path.stat().st_mtime) for fi in self.file_items
        )

    @property
    def last_modified_date_str(self) -> str:
        return (
            format_datetime(self.last_modified_date)
            if self.last_modified_date
            else "Never"
        )

    @computed_field  # type: ignore[prop-decorator]
    @property
    def size_bytes(self) -> int:
        """Get the total size in bytes of all files in the bundle"""
        return sum(fi.path.stat().st_size for fi in self.file_items)

    @property
    def size_str(self) -> str:
        return format_file_size(self.size_bytes)

    @computed_field  # type: ignore[prop-decorator]
    @property
    def word_count(self) -> int:
        """Get the total word count of all files in the bundle"""
        return sum(compute_word_count(read_file(fi.path)) for fi in self.file_items)

    @property
    def is_stale(self) -> bool:
        """Check if bundle is stale (files modified after last export)"""
        if not self.metadata.export_stats.last_exported:
            return False  # Never exported, so not stale

        if not self.last_modified_date:
            return False  # No files with modification dates

        return self.last_modified_date > self.metadata.export_stats.last_exported

    def prune(self):
        """Remove files that no longer exist from a bundle"""
        original_count = len(self.file_items)
        self.file_items = [fi for fi in self.file_items if fi.path.exists()]

        removed_count = original_count - len(self.file_items)
        if removed_count > 0:
            warninig_msg = (
                f"Removed {removed_count} missing files from bundle '{self.name}'"
            )
            logger.warning(warninig_msg)
            show_temp_notification(warninig_msg, type="warning")

    # FUTURE TODO, not now: create XML with a library so it handles special characters and such
    @property
    def code_export(self):
        filtered_items = (fi for fi in self.file_items if not fi.is_dir)
        return f"""<?xml version="1.0" encoding="UTF-8"?>
<documents bundle-name="{self.name}">
{"\n".join(make_file_section(file_item, i) for i, file_item in enumerate(filtered_items))}
</documents>"""


# based on https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/long-context-tips#example-multi-document-structure
# https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/use-xml-tags
def make_file_section(file_item: FileItem, index: int):
    # NOTE we could add error handling

    return f"""    <document index="{index}">
        <source>
            {file_item}
        </source>
        <document_content>
{read_file(file_item.path)}
        </document_content>
    </document>"""
