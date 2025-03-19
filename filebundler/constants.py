# filebundler/constants.py
import os
import logging

from typing import Literal, Optional
from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class EnvironmentSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", case_sensitive=False)

    env: Literal["dev", "prod"] = "prod"
    log_level: Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"] = "WARNING"
    anthropic_api_key: Optional[str] = None

    @field_validator("log_level", mode="before")
    def validate_log_level(cls, value: str) -> str:
        return value.upper()

    @property
    def is_dev(self) -> bool:
        return self.env == "dev"


env_settings = EnvironmentSettings()
if env_settings.is_dev:
    os.environ["ANTHROPIC_API_KEY"] = env_settings.anthropic_api_key

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
    ".mypy_cache/**",
    ".pytest_cache/**",
    "*credentials.json",
]

DISPLAY_NR_OF_RECENT_PROJECTS = 5
SELECTIONS_BUNDLE_NAME = "default-bundle"
