from flask import Flask, g
from flask_cors import CORS

# from routes.cars import car_bp
# from routes.roles import role_bp
from routes.users import user_bp
from routes.bookings import booking_bp
from routes.parkings import parking_bp

# from routes.userroles import userrole_bp
# from routes.transactions import transaction_bp
# from routes.subscriptions import subscription_bp
from whiskey import SimpleMiddleware
from db.models import init_db, SessionLocal

app = Flask(__name__)
CORS(app)

# Uncomment for production
app.wsgi_app = SimpleMiddleware(app.wsgi_app)

# REDO to this format instead of @
# def db_session():
#     ses = SessionLocal()
#     yield ses
#     ses.close()

# with db_session() as ses:


@app.before_request
def create_session():
    g.db = SessionLocal()


@app.teardown_request
def shutdown_session(exception=None):
    db = g.pop("db", None)
    if db is not None:
        db.close()


# Register blueprints for all models
app.register_blueprint(user_bp, url_prefix="/users")
# app.register_blueprint(role_bp)
# app.register_blueprint(subscription_bp)
# app.register_blueprint(car_bp, url_prefix="/cars")
# app.register_blueprint(transaction_bp, url_prefix="/transactions")
# app.register_blueprint(userrole_bp, url_prefix="/userroles")
app.register_blueprint(booking_bp, url_prefix="/bookings")
app.register_blueprint(parking_bp, url_prefix="/parkings")


if __name__ == "__main__":
    init_db()
    app.run(debug=True, host="127.0.0.1", port=5000)
