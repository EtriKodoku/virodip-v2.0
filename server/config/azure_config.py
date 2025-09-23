import os
from dotenv import load_dotenv

load_dotenv()

class AzureStorageConfig:
    AZURE_STORAGE_CONNECTION_STRING = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
    AZURE_STORAGE_ACCOUNT_NAME = os.getenv("AZURE_STORAGE_ACCOUNT_NAME")
    AZURE_STORAGE_ACCOUNT_KEY = os.getenv("AZURE_STORAGE_ACCOUNT_KEY")

class AzureConfig:
    BASIC_AUTH_USERNAME = os.getenv("AUTH_USERNAME")
    BASIC_AUTH_PASSWORD = os.getenv("AUTH_PASSWORD")
    AZURE_CLIENT_ID = os.getenv("AZURE_CLIENT_ID")
    AZURE_TENANT_ID = os.getenv("AZURE_TENANT_ID")
    AZURE_TENANT_NAME = os.getenv("AZURE_TENANT_NAME")
    AZURE_CLIENT_SECRET = os.getenv("AZURE_CLIENT_SECRET")
    AZURE_EXTENSION_APP_ID = os.getenv("AZURE_EXTENSION_APP_ID")

azure_config=AzureConfig()
azure_storage_config=AzureStorageConfig()
