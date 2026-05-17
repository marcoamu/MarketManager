"""
Configuration management using Pydantic for type-safe environment variables.
"""
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field, field_validator
from typing import Optional
from pathlib import Path
import platform


class TradingConfig(BaseSettings):
    """Trading configuration combining both Alpaca services."""
    model_config = SettingsConfigDict(
        env_file="/home/rag/MarketManager/.env",
        env_file_encoding="utf-8",
        extra="ignore",
        env_prefix=""
    )

    # Data service credentials
    alpaca_data_api_key: str = Field(alias="ALPACA_DATA_API_KEY")
    alpaca_data_api_secret: str = Field(alias="ALPACA_DATA_API_SECRET")
    alpaca_data_base_url: str = Field(default="https://paper-api.alpaca.markets", alias="ALPACA_DATA_BASE_URL")
    alpaca_data_paper_mode: bool = Field(default=True, alias="ALPACA_DATA_PAPER_MODE")

    # Bot trading credentials
    alpaca_bot_api_key: str = Field(alias="ALPACA_BOT_API_KEY")
    alpaca_bot_api_secret: str = Field(alias="ALPACA_BOT_API_SECRET")
    alpaca_bot_base_url: str = Field(default="https://paper-api.alpaca.markets", alias="ALPACA_BOT_BASE_URL")
    alpaca_bot_paper_mode: bool = Field(default=True, alias="ALPACA_BOT_PAPER_MODE")


class TelegramConfig(BaseSettings):
    """Telegram service configuration."""
    model_config = SettingsConfigDict(
        env_file="/home/rag/MarketManager/.env",
        env_file_encoding="utf-8",
        extra="ignore",
        env_prefix=""
    )

    telegram_app_id: str = Field(alias="TELEGRAM_APP_ID")
    telegram_app_api_hash: str = Field(alias="TELEGRAM_APP_API_HASH")
    telegram_token_bot: str = Field(alias="TELEGRAM_TOKEN_BOT")
    telegram_token_bot_alt: Optional[str] = Field(default=None, alias="TELEGRAM_TOKEN_BOT_ALT")
    telegram_phone_number: str = Field(alias="TELEGRAM_PHONE_NUMBER")
    telegram_chat_id: int = Field(alias="TELEGRAM_CHAT_ID")
    telegram_group_id: int = Field(alias="TELEGRAM_GROUP_ID")


class DatabaseConfig(BaseSettings):
    """Database configuration."""
    model_config = SettingsConfigDict(
        env_file="/home/rag/MarketManager/.env",
        env_file_encoding="utf-8",
        extra="ignore",
        env_prefix=""
    )

    db_path: str = Field(default="./data/market.db", alias="DB_PATH")
    db_pool_size: int = Field(default=5, alias="DB_POOL_SIZE")


class AppConfig(BaseSettings):
    """Main application configuration."""
    model_config = SettingsConfigDict(
        env_file="/home/rag/MarketManager/.env",
        env_file_encoding="utf-8",
        extra="ignore",
        env_prefix=""
    )

    app_env: str = Field(default="LINUX", alias="APP_ENV")
    app_debug: bool = Field(default=False, alias="APP_DEBUG")
    app_log_level: str = Field(default="INFO", alias="APP_LOG_LEVEL")

    # Nested configs
    trading: TradingConfig = Field(default_factory=TradingConfig)
    telegram: TelegramConfig = Field(default_factory=TelegramConfig)
    database: DatabaseConfig = Field(default_factory=DatabaseConfig)

    @field_validator('app_env', mode='before')
    @classmethod
    def detect_env(cls, v):
        """Auto-detect environment if not set."""
        if v is None:
            sistema = platform.system()
            return "WINDOWS" if sistema == "Windows" else "LINUX"
        return v

    def get_config_path(self) -> str:
        """Get the appropriate config path based on environment."""
        if self.app_env == "WINDOWS":
            return r"F:\WORK\MarketManager2026\config\config.ini"
        return "/home/rag/MarketManager/config/config.ini"


# Global configuration instance
_config: Optional[AppConfig] = None


def get_config() -> AppConfig:
    """Get or create global configuration instance."""
    global _config
    if _config is None:
        _config = AppConfig()
    return _config


def reset_config():
    """Reset configuration (useful for testing)."""
    global _config
    _config = None
