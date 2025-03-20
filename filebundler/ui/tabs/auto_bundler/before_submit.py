# filebundler/ui/tabs/auto_bundler/before_submit.py
import logfire
import streamlit as st

from filebundler import constants
from filebundler.models.Bundle import Bundle
from filebundler.FileBundlerApp import FileBundlerApp
from filebundler.managers.ProjectSettingsManager import ProjectSettingsManager

from filebundler.services.project_structure import save_project_structure

from filebundler.ui.notification import show_temp_notification
from filebundler.ui.components.selectable_file_items import (
    render_selectable_file_items_list,
)

from filebundler.lib.llm.claude import ANTHROPIC_MODEL_NAMES
from filebundler.lib.llm.auto_bundle import request_auto_bundle


def render_auto_bundler_before_submit_tab(
    app: FileBundlerApp, psm: ProjectSettingsManager
):
    spinner = st.spinner("Preparing files and sending to LLM...")

    # Auto-select files when the tab is opened
    if not st.session_state.get("auto_bundle_initialized", False):
        with logfire.span("initializing auto-bundle tab"):
            msgs = []
            try:
                if app.project_settings.auto_bundle_settings.auto_refresh_project_structure:
                    project_structure_file_path = save_project_structure(app)
                    structure_file_item = app.file_items.get(
                        project_structure_file_path
                    )
                    if (
                        structure_file_item and not structure_file_item.selected
                    ):  # this should always be True because we (re)create the file
                        structure_file_item.selected = True
                        msgs.append("Auto-selected project structure")

                if app.project_settings.auto_bundle_settings.auto_include_bundle_files:
                    for bundle in app.bundles.bundles_dict.values():
                        for file_item in bundle.file_items:
                            if not file_item.selected:
                                file_item.selected = True
                                msgs.append(
                                    f"Auto-selected {len(app.bundles.bundles_dict)} bundle files"
                                )

                if msgs:
                    show_temp_notification(
                        "\n".join(msgs),
                        type="info",
                        duration=5,
                    )

                st.session_state["auto_bundle_initialized"] = True
            except Exception as e:
                logfire.error(
                    f"Error initializing auto-bundle tab: {e}", _exc_info=True
                )
                show_temp_notification(f"Error initializing: {str(e)}", type="error")
                return

    if app.selections.nr_of_selected_files == 0:
        st.info(
            "Select at least one file for the LLM. "
            "For example the project-structure.md or your TODO.md files."
        )
        return

    with st.expander(
        f"Selected files ({app.selections.nr_of_selected_files})", expanded=False
    ):
        render_selectable_file_items_list(
            app,
            key_prefix="auto_bundler",
            from_items=app.selections.selected_file_items,
        )

    # Text area for user prompt
    user_prompt = st.text_area(
        "Enter your prompt for the LLM",
        placeholder="Describe what you're working on and what kind of files you need...",
        value=psm.project_settings.auto_bundle_settings.user_prompt,
        height=150,
        key="auto_bundler_user_prompt",
    )

    if user_prompt:
        psm.project_settings.auto_bundle_settings.user_prompt = user_prompt
        psm.save_project_settings()

    # Model selection
    model_type = st.selectbox(
        "Select LLM model",
        options=ANTHROPIC_MODEL_NAMES,
        index=2
        if constants.env_settings.is_dev
        else 1,  # Default to Haiku 3.5 in dev, Sonnet 3.5 in prod
        key="auto_bundler_model_type",
    )

    disable_button = (
        app.selections.nr_of_selected_files == 0
        or not user_prompt
        # this is no use because the user can re-click before this happens...
        or st.session_state.get("submitting_to_llm", None) is not None
        or st.session_state.get("auto_bundle_response", None) is not None
    )
    # Submit button
    if st.button(
        "Submit to LLM",
        disabled=disable_button,
        key="auto_bundler_submit_to_llm",
    ):
        if not user_prompt or not model_type:
            st.error("The app state is broken - missing user_prompt or model_type")
            return
        st.session_state["submitting_to_llm"] = True
        # BUG not a bug per say, the spinner is shown below the button
        # the button thus remains clickable
        # which is a problem bc the user can click multiple times if they are impatient
        # we need a fix so the user can't click multiple times
        with spinner:
            temp_bundle = Bundle(
                name="temp-auto-bundle",
                file_items=app.selections.selected_file_items,
            )
            auto_bundle_response = request_auto_bundle(
                temp_bundle=temp_bundle, user_prompt=user_prompt, model_type=model_type
            )
            if not auto_bundle_response:
                st.error("Error getting auto-bundle response")
                return
            st.session_state["auto_bundle_response"] = auto_bundle_response
            st.session_state["submitting_to_llm"] = True
            st.rerun()
