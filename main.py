# main.py
import logging
import streamlit as st

from filebundler.state import initialize_session_state

from filebundler.ui.tabs.export_contents import render_export_tab
from filebundler.ui.tabs.selected_files import render_selected_files_tab
from filebundler.ui.tabs.manage_bundles.main import render_manage_bundles_tab

from filebundler.ui.file_tree import render_file_tree
from filebundler.ui.notification import show_temp_notification
from filebundler.ui.project_selection import render_project_selection
from filebundler.ui.sidebar.settings_panel import render_settings_panel


logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


def main():
    try:
        st.set_page_config(page_title="File Bundler", layout="wide")

        initialize_session_state()

        with st.sidebar:
            render_settings_panel(
                st.session_state.app, st.session_state.settings_manager
            )

        st.title("File Bundler")
        st.write(
            "Bundle project files together for prompting, or estimating and optimizing token and context usage."
        )

        col1, col2 = st.columns([1, 2])

        with col1:
            # Project selection section
            render_project_selection()

            # Only show file tree if project is loaded
            if st.session_state.project_loaded:
                render_file_tree(st.session_state.app)

        # Right column with bundle operations and file preview
        with col2:
            # Only show if project is loaded
            if st.session_state.project_loaded:
                tab1, tab2, tab3 = st.tabs(
                    [
                        f"Selected Files ({st.session_state.app.nr_of_selected_files})",
                        "Export Contents",
                        f"Manage Bundles ({st.session_state.app.nr_of_bundles})",
                    ]
                )

                with tab1:
                    render_selected_files_tab(st.session_state.app)

                with tab2:
                    render_export_tab(st.session_state.app)

                with tab3:
                    render_manage_bundles_tab(st.session_state.app)
            else:
                # If no project loaded
                show_temp_notification(
                    "Please open a project to get started", type="info"
                )

    except Exception as e:
        logger.error(f"Application error: {e}", exc_info=True)
        st.error(f"An error occurred: {str(e)}")


if __name__ == "__main__":
    main()
