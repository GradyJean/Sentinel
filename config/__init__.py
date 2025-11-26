import os
from pathlib import Path

from config.loader import load_config
from config.logger import setup_logger

# project root
PROJECT_ROOT = Path(__file__).resolve().parents[1]
# settings
settings = load_config(f"{PROJECT_ROOT}/setting.yaml")
# core os
CORE_OS = "Unix"

if os.sep == '\\':
    CORE_OS = "Windows"

__all__ = [
    "setup_logger",
    "settings",
    "CORE_OS"
]
