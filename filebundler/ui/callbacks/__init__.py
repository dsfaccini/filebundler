# filebundler/ui/callbacks/__init__.py
import logging
import pyperclip
import streamlit as st

from filebundler.ui.bundle_display import render_saved_bundles
from filebundler.ui.notification import show_temp_notification

logger = logging.getLogger(__name__)


def render_manage_bundles_tab():
    """Render the Manage Bundles tab"""
    st.subheader("Manage Bundles")
    bundle_manager = st.session_state.bundle_manager

    # Use the new component to render bundles
    render_saved_bundles(
        bundles=bundle_manager.bundles,
        load_bundle=lambda name: load_bundle_callback(name),
        create_bundle_from_saved=lambda name: create_bundle_from_saved_callback(name),
        delete_bundle=lambda name: delete_bundle_callback(name),
        rename_bundle=lambda old, new: bundle_manager.rename_bundle(old, new),
    )


# Add callback functions for bundle operations
def load_bundle_callback(name):
    """Callback for loading a bundle"""
    try:
        bundle_manager = st.session_state.bundle_manager
        app = st.session_state.app

        message, file_paths = bundle_manager.load_bundle(name)

        # Clear current selections
        app.clear_all_selections()

        # Mark selected files
        loaded_count = 0
        for rel_path in file_paths:
            try:
                full_path = app.project_path / rel_path
                if full_path in app.file_items:
                    file_item = app.file_items[full_path]
                    file_item.selected = True
                    app.selected_file_paths.add(full_path)
                    loaded_count += 1
            except Exception as e:
                logger.error(f"Error loading path {rel_path}: {e}", exc_info=True)

        # Save selections
        app.save_selections()

        show_temp_notification(
            f"Loaded {loaded_count} of {len(file_paths)} files from bundle '{name}'",
            type="success",
        )
        st.rerun()
    except Exception as e:
        logger.error(f"Error loading bundle: {e}", exc_info=True)
        show_temp_notification(f"Error loading bundle: {str(e)}", type="error")


def create_bundle_from_saved_callback(name):
    """Callback for creating a bundle from saved bundle"""
    try:
        bundle_manager = st.session_state.bundle_manager
        bundle_content = bundle_manager.create_bundle_from_saved(name)

        if (
            bundle_content.startswith("Bundle")
            or bundle_content.startswith("The file")
            or bundle_content.startswith("Failed to")
        ):
            logger.warning(f"Bundle export issue: {bundle_content}")
            show_temp_notification(bundle_content, type="error")
        else:
            try:
                pyperclip.copy(bundle_content)
                show_temp_notification(
                    f"Bundle '{name}' exported to clipboard", type="success"
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
    try:
        bundle_manager = st.session_state.bundle_manager
        result = bundle_manager.delete_bundle(name)
        logger.info(f"Bundle deleted: {name}")
        show_temp_notification(result, type="success")
        st.rerun()
    except Exception as e:
        logger.error(f"Error deleting bundle: {e}", exc_info=True)
        show_temp_notification(f"Error deleting bundle: {str(e)}", type="error")
