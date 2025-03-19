# filebundler/ui/tabs/auto_bundler.py
import logfire
import streamlit as st

from filebundler.models.Bundle import Bundle
from filebundler.FileBundlerApp import FileBundlerApp

from filebundler.ui.notification import show_temp_notification
from filebundler.ui.components.selectable_file_items import (
    render_selectable_file_items_list,
)

from filebundler.services.project_structure import generate_project_structure

from filebundler.lib.llm.auto_bundle import AutoBundleResponse, get_system_prompt
from filebundler.lib.llm.claude import (
    ANTHROPIC_MODEL_NAMES,
    anthropic_synchronous_prompt,
)


def render_auto_bundler_tab(app: FileBundlerApp):
    """Render the Auto-Bundle tab."""
    st.header("Auto-Bundle")

    # Auto-select files when the tab is opened
    if not st.session_state.get("auto_bundle_initialized", False):
        with logfire.span("initializing auto-bundle tab"):
            # Generate project structure
            try:
                if app.project_settings.auto_bundle_settings.auto_include_project_structure:
                    project_structure_file_path = generate_project_structure(app)
                    structure_file_item = app.file_items.get(
                        project_structure_file_path
                    )
                    structure_file_item.selected = True

                show_temp_notification(
                    "Auto-selected project structure",
                    type="info",
                    duration=5,
                )

                if app.project_settings.auto_bundle_settings.auto_include_bundle_files:
                    for bundle in app.bundles.bundles.values():
                        for file_item in bundle.file_items:
                            app.selections.select_file(file_item)

                show_temp_notification(
                    f"Auto-selected {len(app.bundles.bundles)} bundle files",
                    type="info",
                    duration=5,
                )

                st.session_state["auto_bundle_initialized"] = True
            except Exception as e:
                logfire.error(
                    f"Error initializing auto-bundle tab: {e}", _exc_info=True
                )
                show_temp_notification(f"Error initializing: {str(e)}", type="error")

    # Display selected files in an expander
    selected_files_count = app.selections.nr_of_selected_files
    if selected_files_count == 0:
        st.warning("No files selected.")
        return

    with st.expander(f"Selected files ({selected_files_count})", expanded=False):
        selected_files = app.selections.selected_file_items
        render_selectable_file_items_list(app, from_items=selected_files)
    # Text area for user prompt
    user_prompt = st.text_area(
        "Enter your prompt for the LLM",
        placeholder="Describe what you're working on and what kind of files you need...",
        height=150,
    )

    # Model selection
    model_type = st.selectbox(
        "Select LLM model",
        options=ANTHROPIC_MODEL_NAMES,
        index=2,  # Default to Claude 3.5 Sonnet
    )

    if st.button(
        "Submit to LLM", disabled=selected_files_count == 0 or not user_prompt
    ):
        if selected_files_count == 0:
            show_temp_notification("No files selected", type="warning")
            return

        if not user_prompt:
            show_temp_notification("Please enter a prompt", type="warning")
            return

        # Create a temporary bundle to get the export code
        with st.spinner("Preparing files and sending to LLM..."):
            try:
                temp_bundle = Bundle(
                    name="temp-auto-bundle",
                    file_items=app.selections.selected_file_items,
                )

                full_prompt = f"""{temp_bundle.export_code()}\n\n{user_prompt}"""

                auto_bundle_response = anthropic_synchronous_prompt(
                    model_type=model_type,
                    system_prompt=get_system_prompt(),
                    user_prompt=full_prompt,
                    result_type=AutoBundleResponse,
                )

            except Exception as e:
                logfire.error(f"Error in auto-bundle process: {e}", _exc_info=True)
                show_temp_notification(f"Error: {str(e)}", type="error")

        with st.expander("The LLM suggested this bundle:", expanded=True):
            new_bundle_name = st.text_input(
                "Enter a name for the new bundle",
                value=auto_bundle_response.name,
            )
            st.subheader(new_bundle_name or auto_bundle_response.name)
            if auto_bundle_response.message:
                st.markdown(f"""LLM Message: 
                            ```{auto_bundle_response.message}```""")
            st.write("Very Likely Useful Files:")
            render_selectable_file_items_list(
                app,
                key_prefix="auto_bundle",
                from_paths=auto_bundle_response.files.very_likely_useful,
            )
            st.markdown("---")
            st.write("Probably Useful Files:")
            render_selectable_file_items_list(
                app,
                key_prefix="auto_bundle",
                from_paths=auto_bundle_response.files.probably_useful,
            )

        st.write(
            "Select the files you want to bundle. You may also select files from the file tree."
        )
        if st.button("When you're done, click here to save the bundle"):
            # TODO
            pass
