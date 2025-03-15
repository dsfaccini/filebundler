# filebundler/ui/tabs/export_contents.py
import logging
import pyperclip
import streamlit as st

from filebundler.models.Bundle import Bundle

from filebundler.FileBundlerApp import FileBundlerApp
from filebundler.ui.notification import show_temp_notification

logger = logging.getLogger(__name__)


def render_export_tab(app: FileBundlerApp):
    """Render the Export Contents tab"""
    st.subheader("Export Contents")

    # Selected files info
    if app.selections.nr_of_selected_files == 0:
        st.warning("No files selected. Please select files to export.")
        return

    st.write(f"{app.selections.nr_of_selected_files} files selected for export.")

    # Add bundle name field for saving
    bundle_name = st.text_input(
        "Bundle name (lowercase, alphanumeric, with hyphens)",
        key="export_bundle_name",
        value=app.bundles.current_bundle.name if app.bundles.current_bundle else "",
        placeholder="my-bundle-name",
    )

    # Create buttons in a row
    btn_cols = st.columns([1, 1])
    with btn_cols[0]:
        if st.button("Export to Clipboard", use_container_width=True):
            if app.selections.nr_of_selected_files == 0:
                show_temp_notification(
                    "No files selected. Please select files to bundle.",
                    type="error",
                )
            else:
                try:
                    bundle = Bundle(
                        name="clipboard-bundle",
                        file_items=app.selections.selected_file_items,
                    )

                    codex = bundle.code_export

                    pyperclip.copy(codex)
                    show_temp_notification(
                        f"Bundle copied to clipboard: {app.selections.nr_of_selected_files} files, {len(codex)} characters",
                        type="success",
                    )
                except Exception as e:
                    logger.error(f"Export error: {e}", exc_info=True)
                    st.error(f"Error exporting bundle: {str(e)}")
    with btn_cols[1]:
        if st.button("Save Bundle", use_container_width=True):
            try:
                if not bundle_name:
                    show_temp_notification(
                        "Please enter a bundle name to save the bundle.", type="warning"
                    )
                    return

                if not app.selections.selected_file_items:
                    show_temp_notification(
                        "No files selected. Please select files to bundle.",
                        type="warning",
                    )
                    return

                new_bundle = app.bundles.save_bundle(
                    bundle_name, app.selections.selected_file_items
                )
                show_temp_notification(
                    f"Bundle '{bundle_name}' saved with {len(new_bundle.file_items)} files.",
                    type="success",
                )

                st.rerun()
            except Exception as e:
                logger.error(f"Save bundle error: {e}", exc_info=True)
                show_temp_notification(f"Error saving bundle: {str(e)}", type="error")

    # Preview section
    st.subheader("Bundle Preview")
    preview_expander = st.expander("Click to preview bundle content")

    if app.bundles.current_bundle:
        with preview_expander:
            try:
                preview_content = app.bundles.current_bundle.code_export
                if preview_content.startswith("No files") or preview_content.startswith(
                    "Failed to"
                ):
                    show_temp_notification(preview_content, type="warning")
                else:
                    st.code(preview_content, language="markdown")
            except Exception as e:
                logger.error(f"Preview error: {e}", exc_info=True)
                st.error(f"Error generating preview: {str(e)}")
