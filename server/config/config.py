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


class DataBaseConfig(Settings):
    DB_CONNECTION: str = "sqlite:///db/db.sqlite3"


class ManagerConfig(Settings):
    OWNER_EMAIL: str = "jhon.doe@example.com"


db_config = DataBaseConfig()
manager_config = ManagerConfig()
