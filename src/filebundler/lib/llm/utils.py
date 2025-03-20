# filebundler/lib/llm/utils.py
import os
import logging

from enum import Enum


logger = logging.getLogger(__name__)


class ProviderApiKey(str, Enum):
    ANTHROPIC = "ANTHROPIC_API_KEY"


def get_api_key(provider: ProviderApiKey) -> str:
    api_key = os.getenv(provider.value)
    if not api_key:
        raise ValueError(f"No API key found for {provider = } in the environment")

    return api_key
