import os
from auth.validation import check_basic_auth, validate_bearer_token
from werkzeug.wrappers import Response
from dotenv import load_dotenv

from config.logs_config import logger

# Load environment variables
load_dotenv()


class SimpleMiddleware:
    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        # Skip preflight CORS and public endpoints
        if environ.get("REQUEST_METHOD") == "OPTIONS" or "public" in environ.get(
            "RAW_URI", ""
        ):
            logger.info("Skipping auth for preflight or public endpoint:", environ)
            return self.app(environ, start_response)

        # Basic Auth for user registration
        elif "users/register" in environ.get("RAW_URI", ""):
            try:
                assert check_basic_auth(environ)
            except AssertionError:
                response = Response(
                    response='{"error": "Unauthorized"}',
                    status=401,
                    content_type="application/json",
                )
                return response(environ, start_response)

        else:
            try:
                auth_header = environ.get("HTTP_AUTHORIZATION", "")
                if auth_header.startswith("Bearer "):
                    token = auth_header.replace("Bearer ", "")
                    token_data = validate_bearer_token(token)
                    environ["token_data"] = token_data
                else:
                    raise ValueError("No Bearer token found")
            except ValueError:
                response = Response(
                    response='{"error": "Unauthorized"}',
                    status=401,
                    content_type="application/json",
                )
                return response(environ, start_response)
            except Exception as e:
                logger.error(f"Error in token validation: {e}")
                response = Response(
                    response='{"error": "Unauthorized"}',
                    status=401,
                    content_type="application/json",
                )
                return response(environ, start_response)

        logger.info(
            f"Incoming request to {environ.get('PATH_INFO')} with token_data: {environ.get('token_data')}"
        )

        return self.app(environ, start_response)
