import base64
from config.azure_config import azure_config  # assuming BASIC_AUTH = {"username": "...", "password": "..."}

def check_basic_auth(request) -> bool:
    # request.headers is usually a dict-like object in Flask/FastAPI/etc.
    print(request)
    auth_header = request.get("HTTP_AUTHORIZATION", "")
    if not auth_header or not auth_header.startswith("Basic "):
        return False

    base64_credentials = auth_header.split(" ")[1]
    try:
        decoded = base64.b64decode(base64_credentials).decode("utf-8")
        print(decoded)
        username, password = decoded.split(":", 1)
    except Exception as e:
        print(e)
        return False

    return (
        username == azure_config.BASIC_AUTH_USERNAME
        and password == azure_config.BASIC_AUTH_PASSWORD
    )
