# filebundler/lib/llm/auto_bundle.py
import logfire

from filebundler.models.Bundle import Bundle
from filebundler.models.llm.AutoBundleResponse import AutoBundleResponse

from filebundler.ui.notification import show_temp_notification

from filebundler.lib.llm.claude import anthropic_synchronous_prompt

# from typing import Literal
# from filebundler.FileBundlerApp import FileBundlerApp


def get_system_prompt() -> str:
    """Returns the system prompt for the LLM."""
    return (
        "You are a requirements engineer for the FileBundler app. "
        "FileBundler helps users to create bundles of files in their project that belong to certain topics. "
        "For example, all files that deal with payments can be added to a bundle called payments. "
        "The user can use these bundles to develop their project by providing relevant context quickly to other assistants or colleagues. "
        "Your mission is to help the user select files in their project that provide relevant context fulfill the user's task. "
        "The user will provide you with information about their project, like the file structure of their project, bundles that they may already have created, and possibly files and their contents that they deem relevant to their task. "
        "You must answer in the JSON format that we provide you with. In this JSON format you may or may not include a message as advise to the user."
    )


def request_auto_bundle(temp_bundle: Bundle, user_prompt: str, model_type: str):
    try:
        full_prompt = f"""{temp_bundle.export_code()}\n\n{user_prompt}"""

        return anthropic_synchronous_prompt(
            model_type=model_type,
            system_prompt=get_system_prompt(),
            user_prompt=full_prompt,
            result_type=AutoBundleResponse,
        )

    except Exception as e:
        logfire.error(f"Error in auto-bundle process: {e}", _exc_info=True)
        show_temp_notification(f"Error: {str(e)}", type="error")
