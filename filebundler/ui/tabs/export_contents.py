# filebundler/ui/tabs/export_contents.py
import logging
import pyperclip
import streamlit as st

from filebundler.ui.notification import show_temp_notification

logger = logging.getLogger(__name__)


def render_export_tab():
    """Render the Export Contents tab"""
    st.subheader("Export Contents")
    bundle_manager = st.session_state.bundle_manager
    app = st.session_state.app

    # Basic bundle creation
    if st.button("Export Contents"):
        try:
            selected_files = [item.path for item in app.get_selected_files()]
            bundle_content = bundle_manager.create_bundle(
                selected_files, app.get_relative_path
            )

            if (
                bundle_content.startswith("No files")
                or bundle_content.startswith("The file")
                or bundle_content.startswith("Failed to")
            ):
                logger.warning(f"Bundle creation issue: {bundle_content}")
                show_temp_notification(bundle_content, type="error")
            else:
                st.session_state.bundle_content = bundle_content
                pyperclip.copy(bundle_content)
                # Success message
                show_temp_notification(
                    f"Bundle created with {len(app.get_selected_files())} files",
                    type="success",
                )
        except Exception as e:
            logger.error(f"Error creating bundle: {e}", exc_info=True)
            show_temp_notification(f"Error creating bundle: {str(e)}", type="error")

    # Save bundle with name
    col2a, col2b = st.columns([3, 1])
    with col2a:
        bundle_name = st.text_input("Bundle Name (lowercase alphanumeric)")
    with col2b:
        if st.button("Save Bundle"):
            try:
                selected_files = [item.path for item in app.get_selected_files()]
                result = bundle_manager.save_bundle(
                    bundle_name, selected_files, app.get_relative_path
                )

                if (
                    result.startswith("No files")
                    or result.startswith("Please")
                    or result.startswith("Bundle name")
                ):
                    logger.warning(f"Bundle save issue: {result}")
                    show_temp_notification(result, type="error")
                else:
                    logger.info(f"Bundle saved: {bundle_name}")
                    show_temp_notification(result, type="success")
            except Exception as e:
                logger.error(f"Error saving bundle: {e}", exc_info=True)
                show_temp_notification(f"Error saving bundle: {str(e)}", type="error")
            st.rerun()

    # Display the bundle content
    if "bundle_content" in st.session_state:
        st.subheader("Bundle Preview")
        st.text_area("Bundle Content", st.session_state.bundle_content, height=300)

        # Copy to clipboard button
        if st.button("Copy to Clipboard"):
            try:
                pyperclip.copy(st.session_state.bundle_content)
                show_temp_notification("Bundle copied to clipboard", type="success")
            except Exception as e:
                logger.error(f"Clipboard error: {e}", exc_info=True)
                show_temp_notification(
                    f"Could not copy to clipboard: {str(e)}", type="error"
                )
                show_temp_notification(
                    "You can manually copy the content from the text area above",
                    type="info",
                )
