# filebundler/FileBundlerApp.py
import logging
import logfire
import streamlit as st

from typing import Dict, List
from pathlib import Path

from filebundler.models.FileItem import FileItem
from filebundler.models.AppProtocol import AppProtocol
from filebundler.models.ProjectSettings import ProjectSettings

from filebundler.managers.BundleManager import BundleManager
from filebundler.managers.SelectionsManager import SelectionsManager

from filebundler.ui.notification import show_temp_notification

from filebundler.utils.project_utils import invalid_path, sort_files

lf = logfire.with_settings(console_log=False)
logger = logging.getLogger(__name__)


# class ProjectManager
class FileBundlerApp(AppProtocol):
    def __init__(self, project_path: Path):
        self.project_path = project_path.resolve()
        self.file_items: Dict[Path, FileItem] = {}
        self.bundles = BundleManager(project_path=self.project_path)
        self.selections = SelectionsManager(app=self)
        self.project_settings = ProjectSettings()

    @property
    def nr_of_files(self):
        return len([fi for fi in self.file_items.values() if not fi.is_dir])

    def refresh(self):
        self.load_project(self.project_path, self.project_settings)

    def load_project(self, project_path: Path, project_settings: ProjectSettings):
        """Load a project directory"""
        self.project_path = Path(project_path).resolve()
        self.project_settings = project_settings

        # Load the directory structure
        root_item = FileItem(
            path=self.project_path,
            project_path=self.project_path,
            children=[],
            parent=None,
            selected=False,
        )
        self.file_items[self.project_path] = root_item
        self.load_directory_recursive(
            self.project_path,
            root_item,
            self.project_settings,
        )

        # Load saved selections for this project if exists
        self.selections.load_selections()

        # Initialize the bundle manager with the project path
        self.bundles.load_bundles(self.project_path)

    def load_directory_recursive(
        self, dir_path: Path, parent_item: FileItem, project_settings: ProjectSettings
    ):
        """
        Recursively load directory structure into a parent/child hierarchy.

        Args:
            dir_path: Directory to scan
            parent_item: Parent FileItem to attach children to
            project_settings: List of glob patterns to ignore
            max_files: Maximum number of files to include

        Returns:
            bool: True if directory has visible content, False otherwise
        """
        try:
            with lf.span(
                "loading directory {dir_path}",
                dir_path=dir_path.relative_to(self.project_path),
                _level="debug",
            ):
                filtered_filepaths: List[Path] = []
                for filepath in dir_path.iterdir():
                    rel_path = filepath.relative_to(self.project_path)
                    if not invalid_path(rel_path, project_settings.ignore_patterns):
                        filtered_filepaths.append(filepath)

                # Apply max_files limit with warning
                if len(filtered_filepaths) > project_settings.max_files:
                    st.warning(
                        f"Directory contains {len(filtered_filepaths)} files, exceeding limit of {project_settings.max_files}. "
                        f"Truncating to {project_settings.max_files} files."
                    )
                    sorted_filepaths = sort_files(filtered_filepaths, project_settings)[
                        : project_settings.max_files
                    ]
                else:
                    sorted_filepaths = sort_files(filtered_filepaths, project_settings)

                has_visible_content = False

                # Process filepaths in a single pass
                for filepath in sorted_filepaths:
                    try:
                        # Create FileItem once and reuse
                        file_item = FileItem(
                            path=filepath,
                            project_path=self.project_path,
                            parent=parent_item,
                            children=[],
                            selected=False,
                        )

                        if filepath.is_dir():
                            # Recursively process subdirectory
                            subdirectory_has_content = self.load_directory_recursive(
                                filepath,
                                file_item,
                                project_settings,
                            )
                            if subdirectory_has_content:
                                self.file_items[filepath] = file_item
                                parent_item.children.append(file_item)
                                has_visible_content = True
                        else:  # File
                            self.file_items[filepath] = file_item
                            parent_item.children.append(file_item)
                            has_visible_content = True

                    except (PermissionError, OSError):
                        show_temp_notification(
                            f"Error accessing {filepath.relative_to(self.project_path)}",
                            type="error",
                        )
                        continue

                # Clean up empty directories (optional, based on your needs)
                if not has_visible_content and dir_path in self.file_items:
                    del self.file_items[dir_path]

                return has_visible_content

        except Exception as e:
            st.error(f"Error loading directory {dir_path}: {str(e)}")
            return False

    def paths_to_file_items(self, paths: List[Path]):
        file_items: List[FileItem] = []
        for file_path in paths:
            file_item = self.file_items.get(file_path.resolve())
            if file_item:
                file_items.append(file_item)
            else:
                logger.warning(
                    f"the following file doesn't exist in the app: {file_path.resolve()}"
                )
                #             show_temp_notification(
                #                 f"The following file doesn't exist in the app: {file_path.resolve()}. "
                #                 f"""Reasons why you may be seeing this notification:
                # - because an LLM response included a file that was not in the app
                # - because the file was removed and the app has not been refreshed
                # - because a bundle that loaded contained a file that was deleted""",
                #                 type="error",
                #             )
                continue
        return file_items
