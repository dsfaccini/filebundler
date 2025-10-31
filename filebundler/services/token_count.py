# filebundler/services/token_count.py
from filebundler.services.cached_operations import get_tiktoken_encoder


def compute_word_count(text: str):
    """Compute the word count in the given text"""
    return len(text.split())


def count_tokens(text: str, model: str = "o200k_base") -> int:
    """
    Count the number of tokens in the text using cached tiktoken encoder.

    Args:
        text: The text to count tokens for
        model: The tokenizer model to use (default: o200k_base for GPT-4)

    Returns:
        Number of tokens in the text
    """
    encoder = get_tiktoken_encoder(model)
    return len(encoder.encode(text))
