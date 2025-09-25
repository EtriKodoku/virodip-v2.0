import os
from auth.validation import validate_token
from werkzeug.wrappers import Response
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


# TODO
class SimpleMiddleware:
    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        # Пропускаємо preflight CORS та публічні endpoint-и
        if (
            environ.get("REQUEST_METHOD")
            == "OPTIONS"
            # or ("users" in environ.get("RAW_URI", ""))
            # or "cars" in environ.get("RAW_URI", "")
            # or "transactions" in environ.get("RAW_URI", "")
            # or ("public" in environ.get("RAW_URI", ""))
        ):
            return self.app(environ, start_response)
        try:
            auth_header = environ.get("HTTP_AUTHORIZATION", "")
            if auth_header.startswith("Bearer "):
                token = auth_header.replace("Bearer ", "")
                token_data = validate_token(token)
                environ["token_data"] = token_data
            elif auth_header == f"ESP32 {os.getenv('ESP_32')}":
                environ["token_data"] = auth_header
            else:
                raise ValueError("No Bearer token found")
        except Exception as e:
            response = Response(
                response='{"error": "Unauthorized"}',
                status=401,
                content_type="application/json",
            )
            return response(environ, start_response)

        print(
            f"Incoming request to {environ.get('PATH_INFO')} with token_data: {environ.get('token_data')}"
        )
        return self.app(environ, start_response)
