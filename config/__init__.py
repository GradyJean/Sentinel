import os

from config.loader import load_config, PROJECT_ROOT
from config.logger import setup_logger

# project root
PROJECT_ROOT = PROJECT_ROOT
# settings
settings = load_config(f"{PROJECT_ROOT}/setting.yaml")
# core os
CORE_OS = "Unix"

if os.sep == '\\':
    CORE_OS = "Windows"

__all__ = [
    "setup_logger",
    "settings",
    "CORE_OS",
    "PROJECT_ROOT"
]
