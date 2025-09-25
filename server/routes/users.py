import requests
from flask import Blueprint, request, jsonify
from db.models import User
from config.azure_config import azure_config
from utils.graphAPI import create_b2c_user
from utils.roles import get_roles, register_roles

user_bp = Blueprint("user_bp", __name__)


## TODO Registration for peasants
@user_bp.route("/register", methods=["POST"])
def register_user():
    data = request.get_json()
    try:
        user, created = User.get_or_create(  ## TODO Do we need to get_or_create here?
            id=data.get("objectId"),
            name=data.get("displayName"),
            email=data.get("email"),
        )
        roles = get_roles(data.get("email"))
        register_roles(user=user, roles=roles)  ## TODO Handle the result
        result = create_b2c_user(data)  ## TODO Test it
        return {
            "status": 200,
            "jsonBody": {
                "version": "1.0.0",
                "action": "Continue",
                f"extension_{azure_config.AZURE_EXTENSION_APP_ID}_Roles": roles,
            },
        }
    except requests.HTTPError as e:
        return jsonify({"error": str(e), "details": e.response.json()}), 400


@user_bp.route("/delete", methods=["DELETE"])
def delete_user():
    data = request.get_json()
    user_id = data.get("userId")
    if not user_id:
        return jsonify({"error": "userId is required"}), 400
    try:
        # Implement the logic to delete the user from Azure B2C
        # This is a placeholder for actual deletion logic
        return jsonify({"message": f"User {user_id} deleted successfully"}), 200
    except requests.HTTPError as e:
        return jsonify({"error": str(e), "details": e.response.json()}), 400
