# filebundler/ui/tabs/export_contents.py
import logging
import pyperclip
import streamlit as st

from filebundler.FileBundlerApp import FileBundlerApp
from filebundler.ui.notification import show_temp_notification

logger = logging.getLogger(__name__)


def render_export_tab(app: FileBundlerApp):
    """Render the Export Contents tab"""
    st.subheader("Export Contents")

    # Selected files info
    if app.nr_of_selected_files == 0:
        st.warning("No files selected. Please select files to export.")
        return

    st.write(f"{app.nr_of_selected_files} files selected for export.")

    # Add bundle name field for saving
    bundle_name = st.text_input(
        "Bundle name (lowercase, alphanumeric, with hyphens)",
        key="export_bundle_name",
        placeholder="my-bundle-name",
    )

    # Create buttons in a row
    btn_cols = st.columns([1, 1])
    with btn_cols[0]:
        if st.button("Copy to Clipboard", use_container_width=True):
            try:
                selected_files = [item.path for item in app.get_selected_files()]
                bundle_content = app.bundles.create_bundle(selected_files)

                if bundle_content.startswith("No files") or bundle_content.startswith(
                    "Failed to"
                ):
                    st.error(bundle_content)
                else:
                    try:
                        pyperclip.copy(bundle_content)
                        show_temp_notification(
                            f"Bundle copied to clipboard: {app.nr_of_selected_files} files, {len(bundle_content)} characters",
                            type="success",
                        )
                    except Exception as e:
                        logger.error(f"Clipboard error: {e}", exc_info=True)
                        st.error(f"Could not copy to clipboard: {str(e)}")
            except Exception as e:
                logger.error(f"Export error: {e}", exc_info=True)
                st.error(f"Error exporting bundle: {str(e)}")
    with btn_cols[1]:
        if st.button("Save Bundle", use_container_width=True):
            try:
                selected_files = [item.path for item in app.get_selected_files()]
                result = app.bundles.save_bundle(bundle_name, selected_files)
                show_temp_notification(result, type="success")
                # Clear the input field after successful save
                if not result.startswith("No files") and not result.startswith(
                    "Please enter"
                ):
                    # TODO empty the input field after save
                    # we need a different implementation because this one raises an error
                    # streamlit.errors.StreamlitAPIException: `st.session_state.export_bundle_name` cannot be modified after the widget with key `export_bundle_name` is instantiated.
                    # st.session_state.export_bundle_name = ""
                    st.rerun()
            except Exception as e:
                logger.error(f"Save bundle error: {e}", exc_info=True)
                st.error(f"Error saving bundle: {str(e)}")

    # Preview section
    st.subheader("Bundle Preview")
    preview_expander = st.expander("Click to preview bundle content")

    with preview_expander:
        try:
            selected_files = [item.path for item in app.get_selected_files()]
            preview_content = app.bundles.create_bundle(selected_files)
            if preview_content.startswith("No files") or preview_content.startswith(
                "Failed to"
            ):
                st.warning(preview_content)
            else:
                st.code(preview_content, language="markdown")
        except Exception as e:
            logger.error(f"Preview error: {e}", exc_info=True)
            st.error(f"Error generating preview: {str(e)}")
