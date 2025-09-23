import requests
import jwt
from jwt import PyJWKClient
from config.config import db_config

POLICY = "B2C_1_signupsignin"

def get_jwk_client():
    openid_url = f"https://{db_config.AZURE_TENANT_NAME}.b2clogin.com/{db_config.AZURE_TENANT_NAME}.onmicrosoft.com/{POLICY}/v2.0/.well-known/openid-configuration"
    resp = requests.get(openid_url)
    jwks_uri = resp.json()["jwks_uri"]
    return PyJWKClient(jwks_uri)

def validate_token(token):
    jwk_client = get_jwk_client()
    signing_key = jwk_client.get_signing_key_from_jwt(token)
    decoded = jwt.decode(
        token,
        signing_key.key,
        algorithms=["RS256"],
        audience=db_config.AZURE_CLIENT_ID,
        options={"verify_exp": True}
    )
    return decoded

# Usage:
# decoded = validate_token(token)