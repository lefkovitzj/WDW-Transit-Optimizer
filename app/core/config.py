"""
Project Name: WDW-Transit-Optimizer
File Name: app/core/config.py
Description: Web app configuration and environment settings using Pydantic.
Author: Joseph Lefkovitz (github.com/lefkovitzj)
Last Modified: 1/10/2026
"""

# Third-party imports
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    """Configuration settings for the WDW Wayfinder web application."""
    app_name: str = "WDW Wayfinder"
    GRAPH_DATA_PATH: str = "data/wdw_master_graph.json"
    DATABASE_URL: str = "sqlite:///./data/wdw_app.db"
    DEBUG: bool = False
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

settings = Settings()
