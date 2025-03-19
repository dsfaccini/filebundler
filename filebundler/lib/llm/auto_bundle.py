# filebundler/lib/llm/auto_bundle.py
from pathlib import Path
from typing import Optional, List

from pydantic import Field

from filebundler.utils import BaseModel

# from typing import Literal
# from filebundler.models.Bundle import Bundle
# from filebundler.FileBundlerApp import FileBundlerApp


class _AutoBundleResponseFiles(BaseModel):
    """Files categorized by relevance. Keys are 'very_likely_useful' and 'probably_useful', values are lists of file paths."""

    very_likely_useful: List[Path] = Field(
        description="Files that are very likely to be useful. In relative paths."
    )
    probably_useful: List[Path] = Field(
        description="Files that are probably useful. In relative paths."
    )


class AutoBundleResponse(BaseModel):
    """Response structure from the LLM for auto-bundling."""

    name: str = Field(description="Name for the auto-generated bundle")
    files: _AutoBundleResponseFiles = Field(
        description="Files categorized by relevance. Keys are 'very_likely_useful' and 'probably_useful', values are lists of file paths."
    )
    message: Optional[str] = Field(
        default=None,
        description="Optional message with advice or explanation from the LLM",
    )

    def to_bundle():
        # def to_bundle(
        #     self, app: FileBundlerApp, likelihood: Literal["likely", "all"] = "likely"
        # ) -> Bundle:
        #     file_items = [
        #         app.file_items.get(file_path)
        #         for file_path in self.files.very_likely_useful
        #         if file_path in app.file_items
        #     ]
        #     if likelihood == "all":
        #         file_items.extend(
        #             [
        #                 app.file_items.get(file_path)
        #                 for file_path in self.files.probably_useful
        #                 if file_path in app.file_items
        #             ]
        #         )
        #     return Bundle(
        #         name=self.name,
        #         file_items=file_items,
        #     )
        pass


def get_system_prompt() -> str:
    """Returns the system prompt for the LLM."""
    return (
        "You are a requirements engineer for the FileBundler app. "
        "FileBundler helps users to create bundles of files in their project that belong to certain topics. "
        "For example, all files that deal with payments can be added to a bundle called payments. "
        "The user can use these bundles to develop their project by providing relevant context quickly to other assistants or colleagues. "
        "Your mission is to help the user select files in their project that provide relevant context fulfill the user's task. "
        "The user will provide you with information about their project, like the file structure of their project, bundles that they may already have created, and possibly files and their contents that they deem relevant to their task. "
        "You must answer in the JSON format that we provide you with. In this JSON format you may or may not include a message as advise to the user."
    )
