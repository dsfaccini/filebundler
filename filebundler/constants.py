# filebundler/constants.py
import logging

from typing import Literal
from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class EnvironmentSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", case_sensitive=False)
    # env: Literal["dev", "prod"] = "dev"
    log_level: Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"] = "WARNING"

    @field_validator("log_level", mode="before")
    def validate_log_level(cls, value: str) -> str:
        return value.upper()


env_settings = EnvironmentSettings()
LOG_LEVEL = logging._nameToLevel[env_settings.log_level.upper()]

DEFAULT_MAX_RENDER_FILES = 500

DEFAULT_IGNORE_PATTERNS = [
    "venv/**",
    ".venv/**",
    "node_modules/**",
    ".git/**",
    "**/__pycache__/**",
    "package-lock.json",
    "yarn.lock",
    ".DS_Store",
    "**/.ipynb_checkpoints/**",
    "**/.vscode/**",
    "**/.jpg",
    "**/.jpeg",
    "**/.png",
    "**/.gif",
    "**/.pdf",
    "**/.zip",
    "**/.exe",
    "**/.dll",
    "**/.pyc",
    "**/.so",
    "**/.bin",
    "**/.dat",
]

DISPLAY_NR_OF_RECENT_PROJECTS = 5
SELECTIONS_BUNDLE_NAME = "default-bundle"
