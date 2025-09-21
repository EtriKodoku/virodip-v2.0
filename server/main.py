from flask import Flask, request, jsonify, abort
from playhouse.shortcuts import model_to_dict
import uuid
from routes.roles import role_bp
from routes.subscriptions import subscription_bp
from routes.cars import car_bp
from routes.transactions import transaction_bp
from routes.userroles import userrole_bp

app = Flask(__name__)


# Register blueprints for all models
app.register_blueprint(role_bp)
app.register_blueprint(subscription_bp)
app.register_blueprint(car_bp)
app.register_blueprint(transaction_bp)
app.register_blueprint(userrole_bp)

if __name__ == '__main__':
	app.run(debug=True, host='127.0.0.1', port=5000)
