import base64
import hmac

from config.azure_config import azure_config
from config.logs_config import logger


def check_basic_auth(request) -> bool:
    auth_header = request.get("HTTP_AUTHORIZATION", "")
    if not auth_header or not auth_header.startswith("Basic "):
        return False

    base64_credentials = auth_header.split(" ")[1]
    try:
        decoded = base64.b64decode(base64_credentials).decode("utf-8")
        logger.debug(f"Decoded credentials: {decoded}")
        username, password = decoded.split(":", 1)
    except Exception as e:
        logger.error(f"Error decoding credentials: {e}")
        return False

    return username == azure_config.BASIC_AUTH_USERNAME and hmac.compare_digest(
        password, azure_config.BASIC_AUTH_PASSWORD
    )
