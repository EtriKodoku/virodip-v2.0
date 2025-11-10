from datetime import datetime, timedelta
from typing import Dict
from urllib.parse import urlparse

import importlib.util

# Dynamically import azure.storage.blob if available to satisfy linters when package missing
if importlib.util.find_spec("azure.storage.blob") is not None:
    from azure.storage.blob import (
        BlobServiceClient,
        BlobClient,
        generate_blob_sas,
        BlobSasPermissions,
    )
    _HAS_AZURE = True
else:
    BlobServiceClient = None
    BlobClient = None
    generate_blob_sas = None
    BlobSasPermissions = None
    _HAS_AZURE = False

from config.azure_config import azure_storage_config


# Initialize client if config available
_ACCOUNT = azure_storage_config.AZURE_STORAGE_ACCOUNT_NAME
_KEY = azure_storage_config.AZURE_STORAGE_ACCOUNT_KEY

if _HAS_AZURE and _ACCOUNT and _KEY:
    _BLOB_SERVICE = BlobServiceClient(
        account_url=f"https://{_ACCOUNT}.blob.core.windows.net",
        credential=_KEY,
    )
else:
    _BLOB_SERVICE = None


def _parse_permissions(p: str):
    if not _HAS_AZURE or BlobSasPermissions is None:
        raise RuntimeError("azure-storage-blob is not installed; cannot parse permissions")
    perms = BlobSasPermissions()
    if "r" in p:
        perms.read = True
    if "w" in p:
        perms.write = True
    if "c" in p:
        perms.create = True
    if "d" in p:
        perms.delete = True
    return perms


def generate_sas_url(
    container_name: str,
    blob_name: str,
    expires_in_minutes: int = 5,
    permissions: str = "cw",
) -> Dict[str, str]:
    """Return uploadUrl (blob + SAS) and fileUrl (clean blob url).

    permissions is a string like 'r', 'w', 'rw', 'cw' (create+write),
    mapped to BlobSasPermissions.
    """
    if not _HAS_AZURE or _BLOB_SERVICE is None:
        raise RuntimeError("Azure BlobServiceClient is not configured or azure-storage-blob is not installed")

    perms = _parse_permissions(permissions)

    sas_token = generate_blob_sas(
        account_name=_ACCOUNT,
        container_name=container_name,
        blob_name=blob_name,
        account_key=_KEY,
        permission=perms,
        expiry=datetime.utcnow() + timedelta(minutes=expires_in_minutes),
        start=datetime.utcnow() - timedelta(minutes=1),
        protocol="https",
    )

    blob_client = _BLOB_SERVICE.get_blob_client(container=container_name, blob=blob_name)
    upload_url = f"{blob_client.url}?{sas_token}"
    file_url = blob_client.url
    return {"uploadUrl": upload_url, "fileUrl": file_url}


def delete_blob(container_name: str, blob_name: str) -> bool:
    """Delete blob if exists. Returns True if deleted or not present."""
    if not _HAS_AZURE or _BLOB_SERVICE is None:
        raise RuntimeError("Azure BlobServiceClient is not configured or azure-storage-blob is not installed")

    # strip query if user passed full URL
    try:
        parsed = urlparse(blob_name)
        if parsed.scheme and parsed.path:
            # blob_name is actually a URL
            blob_name = parsed.path.split("/")[-1]
    except Exception:
        pass

    blob_client = _BLOB_SERVICE.get_blob_client(container=container_name, blob=blob_name)
    try:
        blob_client.delete_blob()
    except Exception:
        # ignore not found / permission errors here; caller can log if desired
        return False
    return True
