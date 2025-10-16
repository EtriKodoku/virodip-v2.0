import jwt
import hmac
import base64
import requests
from jwt import PyJWKClient

from config.azure_config import azure_config
from config.logs_config import logger


# Constants
B2C_CONFIG_URL = f"https://{azure_config.AZURE_TENANT_NAME}.b2clogin.com/{azure_config.AZURE_TENANT_NAME}.onmicrosoft.com/{azure_config.AZURE_USER_FLOW}/v2.0/.well-known/openid-configuration"


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


def get_jwks_uri():
    metadata = requests.post(B2C_CONFIG_URL).json()
    logger.info(f"Fetched B2C metadata: {metadata}")
    return metadata["jwks_uri"], metadata["issuer"]


def validate_bearer_token(token: str):
    try:
        jwks_uri, issuer = get_jwks_uri()
        jwks_client = PyJWKClient(jwks_uri)
    except Exception as e:
        logger.error(f"Error fetching JWKS: {e}")
        return None
    try:
        signing_key = jwks_client.get_signing_key_from_jwt(token).key
    except Exception as e:
        logger.error(f"Error getting signing key: {e}")
        return None
    try:
        # Verify and decode token
        logger.info(f"Validating token: {token}")
        decoded = jwt.decode(
            token,
            signing_key,
            algorithms=["RS256"],
            audience=azure_config.AZURE_CLIENT_ID,
            issuer=issuer,
        )

        return decoded
    except jwt.ExpiredSignatureError:
        logger.error("Token has expired")
        raise jwt.ExpiredSignatureError("Token has expired")
    except jwt.InvalidAudienceError:
        logger.error("Invalid audience")
        raise jwt.InvalidAudienceError("Invalid audience")
    except jwt.InvalidIssuerError:
        logger.error("Invalid issuer")
        raise jwt.InvalidIssuerError("Invalid issuer")
    except jwt.PyJWTError as e:
        logger.error(f"Token validation error: {e}")
        raise jwt.PyJWTError(f"Token validation error: {e}")
