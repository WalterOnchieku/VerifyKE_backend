"""
VerifyKE application configuration.

This file loads configuration values from environment variables so that
sensitive information and environment-specific settings are not hard-coded
throughout the application.
"""
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):

    # Database connection string.
    DATABASE_URL: str

    # Secret key used later for authentication and JWT tokens.
    SECRET_KEY: str

    # Identifies which environment the application is running in.
    ENVIRONMENT: str = "development"

    # Tell Pydantic Settings to read values from the .env file.
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

settings = Settings()