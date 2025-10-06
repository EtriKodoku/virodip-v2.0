import os
from auth.validation import check_basic_auth
from werkzeug.wrappers import Response
from dotenv import load_dotenv

from config.logs_config import logger

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
            assert check_basic_auth(environ)
        except AssertionError:
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
