"""
Project Name: WDW-Wayfinder
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
    DEBUG: bool = False
    GA4_MEASUREMENT_ID: str = ""
    DATABASE_URL: str = ""
    ENABLE_ANALYTICS: bool = False
    PRODUCTION_URL: str = ""
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

settings = Settings()
