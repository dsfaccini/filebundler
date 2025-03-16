# filebundler/services/code_export_service.py
import logging
import pyperclip

from enum import Enum
from typing import List

from filebundler.constants import SELECTIONS_BUNDLE_NAME

from filebundler.models.Bundle import Bundle
from filebundler.models.FileItem import FileItem
from filebundler.ui.notification import show_temp_notification

logger = logging.getLogger(__name__)


def export_code_from_bundle(bundle: Bundle):
    try:
        pyperclip.copy(bundle.code_export)
        show_temp_notification(
            f"Bundle '{bundle.name}' exported to clipboard", type="success"
        )
    except Exception as e:
        logger.error(f"Clipboard error: {e}", exc_info=True)
        show_temp_notification(f"Could not copy to clipboard: {str(e)}", type="error")


class ExecutionEnvironment(str, Enum):
    UI = "ui"
    CLI = "cli"


def export_code_from_selections(
    selected_file_items: List[FileItem],
    execution_environment: ExecutionEnvironment = ExecutionEnvironment.UI,
):
    try:
        bundle = Bundle(
            name=SELECTIONS_BUNDLE_NAME,
            file_items=selected_file_items,
        )

        if ExecutionEnvironment(execution_environment) == ExecutionEnvironment.UI:
            pyperclip.copy(bundle.code_export)
            show_temp_notification(
                f"Contents copied to clipboard: {len(selected_file_items)} files, {len(bundle.code_export)} characters",
                type="success",
            )
        return bundle
    except Exception as e:
        logger.error(f"Error exporting selections: {e}", exc_info=True)
        show_temp_notification(f"Error exporting selections: {str(e)}", type="error")
