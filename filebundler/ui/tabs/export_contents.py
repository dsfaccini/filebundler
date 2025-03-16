# filebundler/ui/tabs/export_contents.py
import logging
import streamlit as st

from filebundler.FileBundlerApp import FileBundlerApp
from filebundler.services.code_export_service import export_code_from_selections
from filebundler.ui.notification import show_temp_notification

logger = logging.getLogger(__name__)


def render_export_contents_tab(app: FileBundlerApp):
    if app.selections.nr_of_selected_files == 0:
        st.warning("No files selected. Please select files to export.")
        return

    st.write(f"{app.selections.nr_of_selected_files} files selected for export.")

    # Create buttons in a row
    if st.button("Show Preview - Copy to Clipboard", use_container_width=True):
        if app.selections.nr_of_selected_files == 0:
            show_temp_notification(
                "No files selected. Please select files to bundle.",
                type="warning",
            )
        else:
            # copies the contents to clipboard and show notification
            selections_bundle = export_code_from_selections(
                app.selections.selected_file_items
            )

            if selections_bundle:
                st.subheader("Export Preview")
                preview_expander = st.expander("Expand preview")

                with preview_expander:
                    try:
                        # st.code(selections_bundle.code_export, language="markdown")
                        st.code(selections_bundle.code_export, language="xml")
                    except Exception as e:
                        logger.error(f"Preview error: {e}", exc_info=True)
                        st.error(f"Error generating preview: {str(e)}")
