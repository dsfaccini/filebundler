# main.py
import logging
import streamlit as st

from filebundler.constants import LOG_LEVEL
from filebundler.state import initialize_session_state

from filebundler.ui.tabs.manage_bundles import render_saved_bundles
from filebundler.ui.tabs.selected_files import render_selected_files_tab
from filebundler.ui.tabs.export_contents import render_export_contents_tab
from filebundler.ui.tabs.global_settings_panel import render_global_settings

from filebundler.ui.sidebar.file_tree import render_file_tree
from filebundler.ui.sidebar.settings_panel import render_settings_panel
from filebundler.ui.sidebar.project_selection import render_project_selection

from filebundler.ui.notification import show_temp_notification


logging.basicConfig(
    level=LOG_LEVEL, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


def main():
    try:
        st.set_page_config(page_title="File Bundler", layout="wide")

        initialize_session_state()

        with st.sidebar:
            (tab1, tab2) = st.tabs(["Project", "Project Settings"])
            with tab1:
                render_project_selection(
                    st.session_state.global_settings_manager.settings
                )
                if st.session_state.project_loaded:
                    render_file_tree(st.session_state.app)

            with tab2:
                if st.session_state.project_loaded:
                    render_settings_panel(st.session_state.project_settings_manager)
                else:
                    st.warning("Please open a project to configure settings.")

        st.write(
            "Bundle project files together for prompting, or estimating and optimizing token and context usage."
        )
        main_tab1, main_tab2 = st.tabs(["File Bundler", "Global Settings"])
        with main_tab1:
            # Only show if project is loaded
            if st.session_state.project_loaded:
                tab1, tab2, tab3 = st.tabs(
                    [
                        f"Selected Files ({st.session_state.app.selections.nr_of_selected_files})",
                        "Export Contents",
                        f"Manage Bundles ({st.session_state.app.bundles.nr_of_bundles})",
                    ]
                )

                with tab1:
                    render_selected_files_tab(st.session_state.app)

                with tab2:
                    render_export_contents_tab(st.session_state.app)

                with tab3:
                    render_saved_bundles(st.session_state.app.bundles)
            else:
                # If no project loaded
                show_temp_notification(
                    "Please open a project to get started", type="info"
                )
        with main_tab2:
            render_global_settings(st.session_state.global_settings_manager)

    except Exception as e:
        logger.error(f"Application error: {e}", exc_info=True)
        st.error(f"An error occurred: {str(e)}")


if __name__ == "__main__":
    main()
