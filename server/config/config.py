import os
from dotenv import load_dotenv

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
load_dotenv()

class DataBaseConfig:
    DB_PATH = os.getenv("DB_PATH", "sqlite:///app.db")
    
    if not os.path.isabs(DB_PATH):
        DB_PATH = os.path.join(BASE_DIR, DB_PATH)

class ManagerConfig:
    OWNER_EMAIL = os.getenv("OWNER_EMAIL")

db_config=DataBaseConfig()
manager_config=ManagerConfig()