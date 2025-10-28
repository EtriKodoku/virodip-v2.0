import os
from pydantic_settings import BaseSettings
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
ENV_PATH = BASE_DIR / ".env"


class Settings(BaseSettings):
    class Config:
        env_file = ENV_PATH
        env_file_encoding = "utf-8"
        extra = "ignore"


class AzureStorageConfig(Settings):
    AZURE_STORAGE_CONNECTION_STRING: str
    AZURE_STORAGE_ACCOUNT_NAME: str
    AZURE_STORAGE_ACCOUNT_KEY: str


class AzureConfig(Settings):
    BASIC_AUTH_USERNAME: str
    BASIC_AUTH_PASSWORD: str
    AZURE_CLIENT_ID: str
    AZURE_TENANT_ID: str
    AZURE_TENANT_NAME: str
    AZURE_CLIENT_SECRET: str
    AZURE_EXTENSION_APP_ID: str
    AZURE_USER_FLOW: str


azure_config = AzureConfig()
azure_storage_config = AzureStorageConfig()
