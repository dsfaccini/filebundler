"""
Cached operations for file I/O and token counting.
Uses Streamlit's caching for optimal performance in Streamlit apps.
"""

from typing import TypedDict
import streamlit as st
import tiktoken
from pathlib import Path


@st.cache_resource
def get_tiktoken_encoder(model: str = "o200k_base"):
    """
    Get cached tiktoken encoder instance.

    The encoder is expensive to create and is reusable across
    all function calls, so we cache it as a singleton resource.

    Args:
        model: Tiktoken encoding model name

    Returns:
        Tiktoken encoder instance
    """
    return tiktoken.get_encoding(model)


@st.cache_data(ttl=600, max_entries=2000, show_spinner=False)
def get_file_content(file_path: str, mtime: float):
    """
    Get cached file contents with automatic mtime-based invalidation.

    Cache is automatically invalidated when file modification time changes.
    This prevents serving stale content while avoiding excessive file reads.

    Args:
        file_path: Absolute file path as string
        mtime: File modification time (unix timestamp)

    Returns:
        File contents as string, or None if file cannot be read
    """
    from filebundler.utils import read_file

    try:
        return read_file(Path(file_path))
    except (FileNotFoundError, OSError, UnicodeDecodeError):
        return None


@st.cache_data(ttl=3600, max_entries=1000, show_spinner=False)
def get_file_tokens(file_path: str, mtime: float, model: str = "o200k_base") -> int:
    """
    Get cached token count for file with mtime-based invalidation.

    Token counting is expensive, so we cache results for up to 1 hour.
    Cache is automatically invalidated when file is modified.

    Args:
        file_path: Absolute file path as string
        mtime: File modification time (unix timestamp)
        model: Tiktoken encoding model name

    Returns:
        Number of tokens in the file
    """
    content = get_file_content(file_path, mtime)

    if content is None:
        return 0

    encoder = get_tiktoken_encoder(model)
    return len(encoder.encode(content))


@st.cache_data(ttl=60, max_entries=100, show_spinner=False)
def get_total_tokens(
    file_paths: tuple[str, ...],
    mtimes: tuple[float, ...],
    model: str = "o200k_base"
) -> int:
    """
    Get cached total token count for multiple files.

    Used by SelectionsManager to efficiently calculate total tokens
    for selected files. Cache key includes all file paths and mtimes,
    so any file change invalidates the cache.

    Args:
        file_paths: Tuple of absolute file paths
        mtimes: Tuple of corresponding modification times
        model: Tiktoken encoding model name

    Returns:
        Total token count across all files
    """
    total = 0
    for path, mtime in zip(file_paths, mtimes):
        total += get_file_tokens(path, mtime, model)
    return total

# NOTE: this is a utility for debugging, it's never called by the code
def clear_file_caches():
    """Clear all file-related caches. Useful for debugging or manual refresh."""
    get_file_content.clear()  #  pyright: ignore[reportFunctionMemberAccess]
    get_file_tokens.clear()  #  pyright: ignore[reportFunctionMemberAccess]
    get_total_tokens.clear()  #  pyright: ignore[reportFunctionMemberAccess]

class TokenCacheStats(TypedDict):
    file_content_cache: str
    file_tokens_cache: str
    total_tokens_cache: str
    encoder_cache: str

def get_cache_stats() -> TokenCacheStats:
    """
    Get statistics about cache usage.

    Returns:
        Dictionary with cache information
    """
    return {
        "file_content_cache": "active",
        "file_tokens_cache": "active",
        "total_tokens_cache": "active",
        "encoder_cache": "active (singleton)",
    }
