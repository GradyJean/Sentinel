import logging
import os
from pathlib import Path

import yaml
from pydantic import BaseModel, ValidationError

from models.config import ServerConfig, NginxConfig, ElasticsearchConfig, DatabaseConfig

PROJECT_ROOT = Path(__file__).resolve().parents[1]


class Config(BaseModel):
    server: ServerConfig
    nginx: NginxConfig
    elasticsearch: ElasticsearchConfig
    database: DatabaseConfig


def load_config(config_path: str) -> Config:
    if not os.path.exists(config_path):
        logging.error(f"Config file not found: {config_path}")
        raise FileNotFoundError(f"Config file not found: {config_path}")
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)
        config = Config(**data)
        config.database.url = __fix_database_url(config.database.url)
        return config
    except Exception as e:
        logging.error(f"Failed to load or validate config: {e}")
        raise ValidationError(f"Failed to load or validate config: {e}")


def __fix_database_url(url: str) -> str:
    prefix = "sqlite:///"
    if url.startswith(prefix) and not url.startswith("sqlite:////"):
        rel = url[len(prefix):]
        return f"{prefix}{(PROJECT_ROOT / rel).resolve().as_posix()}"
    return url
