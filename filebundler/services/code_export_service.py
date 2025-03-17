# filebundler/services/code_export_service.py
import logging
import pyperclip

from enum import Enum

from filebundler.models.Bundle import Bundle
from filebundler.ui.notification import show_temp_notification

logger = logging.getLogger(__name__)


class ExecutionEnvironment(str, Enum):
    UI = "ui"
    CLI = "cli"


def copy_code_from_bundle(
    bundle: Bundle,
    execution_environment: ExecutionEnvironment = ExecutionEnvironment.UI,
):
    try:
        if ExecutionEnvironment(execution_environment) == ExecutionEnvironment.UI:
            pyperclip.copy(bundle.code_export)
            show_temp_notification(
                f"Contents copied to clipboard: {len(bundle.file_items)} files, {len(bundle.code_export)} characters",
                type="success",
            )
    except Exception as e:
        logger.error(f"Error exporting contents: {e}", exc_info=True)
        show_temp_notification(f"Error exporting contents: {str(e)}", type="error")


# NOTE we can use this file in the future to export contents directly from the CLI
