# filebundler/ui/tabs/manage_bundles/main.py
import logging
import pyperclip
import streamlit as st

from filebundler.FileBundlerApp import FileBundlerApp

from filebundler.ui.notification import show_temp_notification
from filebundler.ui.tabs.manage_bundles.bundle_display import render_saved_bundles

logger = logging.getLogger(__name__)


def render_manage_bundles_tab(app: FileBundlerApp):
    """Render the Manage Bundles tab"""
    st.subheader(f"Manage Bundles ({st.session_state.app.nr_of_bundles})")

    # Use the new component to render bundles
    render_saved_bundles(
        bundles=app.bundles.bundles,
        load_bundle=lambda name: activate_bundle_callback(name),
        create_bundle_from_saved=lambda name: create_bundle_from_saved_callback(name),
        delete_bundle=lambda name: delete_bundle_callback(name),
        # rename_bundle=lambda old, new: app.bundles.rename_bundle(old, new),
    )


def activate_bundle_callback(name):
    """Callback for loading a bundle"""
    try:
        app: FileBundlerApp = st.session_state.app

        bundle = app.bundles._find_bundle_by_name(name)
        if not bundle:
            show_temp_notification(f"Bundle '{name}' not found", type="error")
            return

        # Clear current selections
        app.clear_all_selections()

        # Mark selected files
        loaded_count = 0
        for rel_path in bundle.file_paths:
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
            f"Loaded {loaded_count} of {len(bundle.file_paths)} files from bundle '{name}'",
            type="success",
        )
        st.rerun()
    except Exception as e:
        logger.error(f"Error loading bundle: {e}", exc_info=True)
        show_temp_notification(f"Error loading bundle: {str(e)}", type="error")


def create_bundle_from_saved_callback(name):
    """Callback for creating a bundle from saved bundle"""
    try:
        app: FileBundlerApp = st.session_state.app
        bundle_content = app.bundles.create_bundle_from_saved(name)

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
