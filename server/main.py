import time
import uuid
import json
from flask import Flask, g, request
from flask_cors import CORS
from flasgger import Swagger

# from routes.cars import car_bp
# from routes.roles import role_bp
from routes.users import user_bp
from routes.bookings import booking_bp
from routes.parkings import parking_bp
# from routes.userroles import userrole_bp
# from routes.transactions import transaction_bp
# from routes.subscriptions import subscription_bp

from config.logs_config import logger
from whiskey import SimpleMiddleware
from db.models import init_db, SessionLocal


def create_app():
    """Фабрика Flask-додатку."""  # changed: додано docstring
    app = Flask(__name__)
    CORS(app)  # changed: переніс сюди, щоб усе було в одному місці
    #app.wsgi_app = SimpleMiddleware(app.wsgi_app)  # changed: тепер у фабриці

    # --- Swagger конфігурація ---
    swagger_config = {
        "headers": [],
        "specs": [
            {
                "endpoint": "apispec",
                "route": "/docs/apispec.json",
                "rule_filter": lambda rule: True,
                "model_filter": lambda tag: True,
            }
        ],
        "static_url_path": "/flasgger_static",
        "swagger_ui": True,
        "specs_route": "/docs/",
    }
    Swagger(app, config=swagger_config)  # changed: переніс в межі функції

    # --- Middleware / hooks ---
    @app.before_request
    def create_session():
        g.db = SessionLocal()

    @app.before_request
    def log_request_info():
        """Logs request details before processing."""
        request.start_time = time.time()
        g.request_id = str(uuid.uuid4())
        try:
            data = json.loads(request.data.decode("utf-8") or "{}")
        except Exception:
            data = {}
        logger.info(
            f"Request: {request.method} {request.path} {json.dumps(data, separators=(':', ','))} "
            f"from {request.remote_addr} | Headers: {dict(request.headers)}"
        )

    @app.after_request
    def log_response_info(response):
        duration = time.time() - request.start_time
        logger.info(
            f"Response: {response.status} for {request.method} {request.path} "
            f"from {request.remote_addr} | Duration: {duration:.4f}s | Headers: {dict(response.headers)}"
        )
        return response

    @app.teardown_request
    def shutdown_session(exception=None):
        db = g.pop("db", None)
        if db is not None:
            db.close()

    # --- Blueprints ---
    app.register_blueprint(user_bp, url_prefix="/users")
    app.register_blueprint(booking_bp, url_prefix="/bookings")
    app.register_blueprint(parking_bp, url_prefix="/parkings")
    # app.register_blueprint(role_bp)
    # app.register_blueprint(subscription_bp)
    # app.register_blueprint(car_bp, url_prefix="/cars")
    # app.register_blueprint(transaction_bp, url_prefix="/transactions")
    # app.register_blueprint(userrole_bp, url_prefix="/userroles")

    return app


if __name__ == "__main__":
    init_db()
    app = create_app()  # changed: тепер створюємо додаток через фабрику
    app.run(debug=True, host="127.0.0.1", port=5000)
