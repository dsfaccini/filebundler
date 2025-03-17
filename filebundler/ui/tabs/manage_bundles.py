# filebundler/ui/manage_bundles/bundle_display.py
import logging
import streamlit as st

from filebundler.FileBundlerApp import FileBundlerApp
from filebundler.managers.BundleManager import BundleManager

from filebundler.ui.notification import show_temp_notification
from filebundler.services.code_export_service import copy_code_from_bundle

logger = logging.getLogger(__name__)


def activate_bundle(name: str):
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

        app.selections.save_selections()
        app.bundles.activate_bundle(bundle)

        st.rerun()
        show_temp_notification(
            f"Loaded {loaded_count} of {len(bundle.file_items)} files from bundle '{name}'",
            type="success",
        )
    except Exception as e:
        logger.error(f"Error loading bundle: {e}", exc_info=True)
        show_temp_notification(f"Error loading bundle: {str(e)}", type="error")


def delete_bundle(bundle_manager: BundleManager, name: str):
    """Callback for deleting a bundle"""
    # BUG DONT FIX
    # st.dialog doesn't close, it works by setting state and rerunning the app
    # but I don't want to add the complexity so we leave the delete unchecked
    # if not confirm(f"Delete bundle '{name}'?"):
    #     return
    try:
        bundle_manager.delete_bundle(name)
        st.rerun()
    except Exception as e:
        logger.error(f"Error deleting bundle: {e}", exc_info=True)
        show_temp_notification(f"Error deleting bundle: {str(e)}", type="error")


def render_saved_bundles(bundle_manager: BundleManager):
    """
    Render the list of saved bundles with improved UI and border separation

    Args:
        bundles: List of Bundle objects
    """
    # Add custom CSS for bundle styling
    st.markdown(
        """
    <style>
    /* Bundle container with border and margin */
    .bundle-container {
        border: 1px solid rgba(128, 128, 128, 0.2);
        border-radius: 5px;
        margin-bottom: 15px;
    }
    
    /* Make bundle buttons the same size */
    .bundle-buttons button {
        min-width: 80px !important;
    }
    </style>
    """,
        unsafe_allow_html=True,
    )

    # Display each bundle with border
    for bundle in bundle_manager.bundle_dict.values():
        st.markdown('<div class="bundle-container">', unsafe_allow_html=True)

        bundle_is_active = bundle is bundle_manager.current_bundle
        checkmark = "✅" if bundle_is_active else None

        # Bundle dropdown with files
        with st.expander(
            f'Files in "{bundle.name}" ({len(bundle.file_items)} files)',
            expanded=bundle_is_active,
            icon=checkmark,
        ):
            for file_item in bundle.file_items:
                st.write(f"- {file_item}")

        # Bundle actions with equal-sized buttons
        col1, col2, col3 = st.columns(3)
        with col1:
            activate_bundle_help = """Activating a bundle will select the files in the bundle.
Selecting new files will not automatically add them to the bundle. 
You must manually save the bundle again if you want to add them.
"""
            if st.button(
                "Activate",
                key=f"activate_{bundle.name}",
                use_container_width=True,
                help=activate_bundle_help,
            ):
                activate_bundle(bundle.name)
        with col2:
            if st.button(
                "Copy to Clipboard",
                key=f"create_{bundle.name}",
                use_container_width=True,
                help="Copies the exported contents to clipboard without activating the bundle.",
            ):
                # copies the contents to clipboard and displays notification
                copy_code_from_bundle(bundle)
        with col3:
            if st.button(
                "Delete", key=f"delete_{bundle.name}", use_container_width=True
            ):
                delete_bundle(bundle_manager, bundle.name)

        st.markdown("</div>", unsafe_allow_html=True)
    if not bundle_manager.bundle_dict:
        st.warning("No saved bundles to display.")
