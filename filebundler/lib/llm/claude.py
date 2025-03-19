# filebundler/lib/llm/claude.py
import logfire

from typing import TypeVar, Type

from pydantic_ai import Agent
from pydantic_ai.models.anthropic import AnthropicModel
from pydantic_ai.models.anthropic import AnthropicModelName
from pydantic_ai.providers.anthropic import AnthropicProvider

from filebundler.utils import BaseModel
import filebundler.lib.llm.utils as llm_utils


# NOTE sadly we need to maintain these manually
ANTHROPIC_MODEL_NAMES = [
    "claude-3-7-sonnet-latest",
    "claude-3-5-haiku-latest",
    "claude-3-5-sonnet-latest",
    "claude-3-opus-latest",
]

T = TypeVar("T", bound=BaseModel)


def anthropic_synchronous_prompt(
    model_type: AnthropicModelName,
    system_prompt: str,
    user_prompt: str,
    result_type: Type[T],
):
    """
    Send a prompt to the LLM and get a structured response.

    Args:
        model_type: The LLM model to use
        system_prompt: The system prompt text
        user_prompt: The user's prompt text

    Returns:
        Structured response from the LLM
    """
    api_key = llm_utils.get_api_key(llm_utils.ProviderApiKey.ANTHROPIC)
    with logfire.span(
        "prompting LLM for auto-bundle", model=model_type.value, _level="info"
    ):
        model = AnthropicModel(
            # ModelType(model_type).value #  we don't validte here bc the options come from the selectbox
            model_type,
            provider=AnthropicProvider(api_key=api_key),
        )
        agent = Agent(
            model,
            result_type=result_type,
            system_prompt=system_prompt,
        )

        try:
            response = agent.run_sync(user_prompt)
            logfire.info(
                "LLM response received",
                token_usage=response.usage,
            )
            return response.data

        except Exception as e:
            logfire.error(f"Error prompting LLM: {str(e)}", _exc_info=True)
            raise
