from datetime import datetime, timedelta
from typing import Dict
from urllib.parse import urlparse
from azure.storage.blob import (
    BlobServiceClient,
    generate_blob_sas,
    BlobSasPermissions,
)
from config.azure_config import azure_storage_config


# Initialize client if config available
_ACCOUNT = azure_storage_config.AZURE_STORAGE_ACCOUNT_NAME
_KEY = azure_storage_config.AZURE_STORAGE_ACCOUNT_KEY


_BLOB_SERVICE = BlobServiceClient(
    account_url=f"https://{_ACCOUNT}.blob.core.windows.net",
    credential=_KEY,
)

def generate_sas_url(
    container_name: str,
    blob_name: str,
    expires_in_minutes: int = 5,
    permissions: str = "cw",
) -> Dict[str, str]:

    perms = BlobSasPermissions.from_string(permissions)

    sas_token = generate_blob_sas(
        account_name=_ACCOUNT,
        container_name=container_name,
        blob_name=blob_name,
        account_key=_KEY,
        permission=perms,
        start=datetime.utcnow() - timedelta(minutes=1),
        expiry=datetime.utcnow() + timedelta(minutes=expires_in_minutes),
        protocol="https",
    )

    blob_client = _BLOB_SERVICE.get_blob_client(
        container=container_name,
        blob=blob_name,
    )

    return {
        "uploadUrl": f"{blob_client.url}?{sas_token}",
        "fileUrl": blob_client.url,
    }


def delete_blob(container_name: str, blob_name: str) -> bool:
    """Delete blob if exists. Returns True if deleted or not present."""

    # strip query if user passed full URL
    try:
        parsed = urlparse(blob_name)
        if parsed.scheme and parsed.path:
            # blob_name is actually a URL
            blob_name = parsed.path.split("/")[-1]
    except Exception:
        pass

    blob_client = _BLOB_SERVICE.get_blob_client(
        container=container_name, blob=blob_name
    )
    try:
        blob_client.delete_blob()
    except Exception:
        return False
    return True
