# filebundler/ui/tabs/manage_bundles/main.py
import logging
import pyperclip
import streamlit as st

from filebundler.FileBundlerApp import FileBundlerApp

from filebundler.models.Bundle import Bundle
from filebundler.ui.notification import show_temp_notification
from filebundler.ui.tabs.manage_bundles.display_bundles import render_saved_bundles

logger = logging.getLogger(__name__)


def render_manage_bundles_tab(app: FileBundlerApp):
    """Render the Manage Bundles tab"""
    st.subheader(f"Manage Bundles ({st.session_state.app.bundles.nr_of_bundles})")

    # Use the new component to render bundles
    render_saved_bundles(
        bundle_manager=app.bundles,
        activate_bundle=lambda name: activate_bundle_callback(name),
        export_code_from_bundle=lambda name: export_code_from_bundle_callback(name),
        delete_bundle=lambda name: delete_bundle_callback(name),
        # rename_bundle=lambda old, new: app.bundles.rename_bundle(old, new),
    )


def activate_bundle_callback(name: str):
    """Callback for loading a bundle"""
    try:
        app: FileBundlerApp = st.session_state.app
        bundle = app.bundles._find_bundle_by_name(name)

        if not bundle:
            show_temp_notification(f"Bundle '{name}' not found", type="error")
            return

        # Clear current selections
        app.selections.clear_all_selections()

        # Mark selected files
        loaded_count = 0
        for file_item in bundle.file_items:
            corresponding_file_item = app.file_items.get(file_item.path)
            if not corresponding_file_item:
                warning_msg = (
                    f"File item not found in this project: {file_item.path = }"
                )
                logger.warning(warning_msg)
                show_temp_notification(warning_msg, type="warning")
                continue
            else:
                corresponding_file_item.selected = True
                loaded_count += 1

        # Save selections
        app.selections.save_selections()

        show_temp_notification(
            f"Loaded {loaded_count} of {len(bundle.file_items)} files from bundle '{name}'",
            type="success",
        )
        st.rerun()
    except Exception as e:
        logger.error(f"Error loading bundle: {e}", exc_info=True)
        show_temp_notification(f"Error loading bundle: {str(e)}", type="error")


def export_code_from_bundle_callback(bundle: Bundle):
    """Callback for creating a bundle from saved bundle"""
    try:
        if (
            bundle.code_export.startswith("Bundle")
            or bundle.code_export.startswith("The file")
            or bundle.code_export.startswith("Failed to")
        ):
            logger.warning(f"Bundle export issue: {bundle.code_export}")
            show_temp_notification(bundle.code_export, type="error")
        else:
            try:
                pyperclip.copy(bundle.code_export)
                show_temp_notification(
                    f"Bundle '{bundle.name}' exported to clipboard", type="success"
                )
            except Exception as e:
                logger.error(f"Clipboard error: {e}", exc_info=True)
                show_temp_notification(
                    f"Could not copy to clipboard: {str(e)}", type="error"
                )
    except Exception as e:
        logger.error(f"Error exporting bundle: {e}", exc_info=True)
        show_temp_notification(f"Error exporting bundle: {str(e)}", type="error")


def delete_bundle_callback(name):
    """Callback for deleting a bundle"""
    # BUG DONT FIX
    # st.dialog doesn't close, it works by setting state and rerunning the app
    # but I don't want to add the complexity so we leave the delete unchecked
    # if not confirm(f"Delete bundle '{name}'?"):
    #     return
    try:
        app: FileBundlerApp = st.session_state.app
        result = app.bundles.delete_bundle(name)
        logger.info(f"Bundle deleted: {name}")
        show_temp_notification(result, type="success")
        st.rerun()  # Add rerun to update UI after deletion
    except Exception as e:
        logger.error(f"Error deleting bundle: {e}", exc_info=True)
        show_temp_notification(f"Error deleting bundle: {str(e)}", type="error")
