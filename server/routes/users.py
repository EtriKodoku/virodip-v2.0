import requests
from flask import Blueprint, request, jsonify, g

from db.models import User, Car
from config.azure_config import azure_config
from config.logs_config import logger
from utils.graphAPI import create_b2c_user
from utils.roles import get_roles, register_roles, can_assign_roles
from utils.blob_service import delete_blob, generate_sas_url

from typing import cast
from cast_types.g_types import DbSessionType

#   Add this line to every endpoint for enabling hints
#   db: DbSessionType = cast(DbSessionType, g.db)


user_bp = Blueprint("user_bp", __name__)


## Register user
@user_bp.route("/register", methods=["POST"])
def register_user():
    data = request.get_json()
    db: DbSessionType = g.db
    try:

        # Check if user exists
        user = db.query(User).filter_by(id=data.get("objectId")).first()
        if not user:
            # Create new user
            user = User(
                id=data.get("objectId"),
                name=data.get("displayName"),
                email=data.get("email"),
            )
            db.add(user)
            db.commit()
        else:
            # Update existing user if needed
            user.name = data.get("displayName")
            user.email = data.get("email")
            db.commit()

        # Handle roles
        roles = get_roles(user.email)
        register_roles(user=user, roles=roles)  # You can handle the result if needed

        # Create B2C user
        # result = create_b2c_user(data)  # Ensure this works as expected

        return {
            "status": 200,
            "jsonBody": {
                "version": "1.0.0",
                "action": "Continue",
                f"extension_{azure_config.AZURE_EXTENSION_APP_ID}_Role": roles,
            },
        }
    except requests.HTTPError as e:
        g.db.rollback()
        logger.error(
            f"HTTP error in user registration: {e}, response: {e.response.json()}"
        )
        return jsonify({"error": str(e), "details": e.response.json()}), 400
    except Exception as e:
        g.db.rollback()
        logger.error(f"Error in user registration: {e}")
        return jsonify({"error": str(e)}), 500


## Delete user by ID
@user_bp.route("/<string:user_id>", methods=["DELETE"])
def delete_user(user_id):
    ##TODO Do we need to delete the user from Azure B2C as well?
    db: DbSessionType = cast(DbSessionType, g.db)

    if not user_id:
        return jsonify({"error": "userId is required"}), 400

    try:

        user = db.query(User).filter_by(id=user_id).first()
        if not user:
            return jsonify({"error": "User not found"}), 404

        db.delete(user)
        db.commit()

        return jsonify({"status": "success", "message": f"User {user_id} deleted"}), 204

    except Exception as e:
        db.rollback()
        return jsonify({"error": str(e)}), 500


## Get all users
@user_bp.route("/", methods=["GET"])
def get_users():
    db: DbSessionType = cast(DbSessionType, g.db)
    try:
        users = db.query(User).all()
        user_list = []

        for user in users:
            roles = [role.name for role in user.roles] if hasattr(user, "roles") else get_roles(user.email)
            user_data = user.to_dict()
            user_data["roles"] = roles
            user_list.append(user_data)

        return jsonify(user_list), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


## Get user by ID
@user_bp.route("/<string:user_id>", methods=["GET"])
def get_user(user_id):
    db: DbSessionType = cast(DbSessionType, g.db)
    try:
        user = db.query(User).filter_by(id=user_id).first()
        if not user:
            return jsonify({"error": "User not found"}), 404

        
        roles = [role.name for role in user.roles] if hasattr(user, "roles") else get_roles(user.email)

        user_data = user.to_dict()
        user_data["roles"] = roles

        return jsonify(user_data), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


## Patch user by ID
@user_bp.route("/<string:user_id>", methods=["PATCH"])
def patch_user(user_id):
    data = request.get_json()
    db: DbSessionType = cast(DbSessionType, g.db)
    if not data:
        return jsonify({"error": "No data provided"}), 400

    try:
        user = db.query(User).filter_by(id=user_id).first()
        if not user:
            return jsonify({"error": "User not found"}), 404
        if "name" in data:
            user.name = data["name"]
        if "email" in data:
            user.email = data["email"]
        if "phoneNumber" in data:
            user.phone_number = data["phoneNumber"]

        db.commit()
        return jsonify(user.to_dict()), 200

    except Exception as e:
        db.rollback()
        return jsonify({"error": str(e)}), 500


## Set user roles
@user_bp.route("/<string:user_id>/roles", methods=["POST", "PUT"])
def set_user_roles(user_id):
    """
    Set roles for a user with access control.
    
    Expects JSON: {"newRoles": ["role1", "role2", ...]} or {"roles": ["role1", "role2", ...]}
    """
    data = request.get_json() or {}
    db: DbSessionType = cast(DbSessionType, g.db)
    
    # Try both possible keys
    new_roles = data.get("newRoles") or data.get("roles") or []
    
    if not isinstance(new_roles, list):
        return jsonify({"error": "roles must be a list"}), 400
    
    # Get current user from g (should be set by auth middleware)
    current_user_id = getattr(g, "user_id", None)
    if not current_user_id:
        return jsonify({"error": "Unauthorized: current user not found"}), 401
    
    try:
        # Get current user
        current_user = db.query(User).filter_by(id=current_user_id).first()
        if not current_user:
            return jsonify({"error": "Current user not found"}), 401
        
        current_user_roles = current_user.get_roles()
        
        # Get target user
        target_user = db.query(User).filter_by(id=user_id).first()
        if not target_user:
            return jsonify({"error": "Target user not found"}), 404
        
        # Check permissions
        can_assign, error_msg = can_assign_roles(current_user_roles, new_roles)
        if not can_assign:
            return jsonify({"error": error_msg}), 403
        
        # Get or create roles in database
        db_roles = []
        for role_name in new_roles:
            role = db.query(Role).filter_by(name=role_name).first()
            if not role:
                role = Role(name=role_name)
                db.add(role)
                db.flush()
            db_roles.append(role)
        
        # Clear existing roles
        db.query(UserRole).filter_by(user_id=user_id).delete()
        db.flush()
        
        # Add new roles
        for role in db_roles:
            user_role = UserRole(user_id=user_id, role_id=role.id)
            db.add(user_role)
        
        db.commit()
        
        # Return updated roles
        updated_roles = target_user.get_roles()
        return jsonify({
            "user_id": user_id,
            "roles": updated_roles
        }), 200
    
    except Exception as e:
        db.rollback()
        logger.error(f"Error setting user roles: {e}")
        return jsonify({"error": str(e)}), 500


### Create car for user
@user_bp.route("/<string:user_id>/cars", methods=["POST"])
def create_car(user_id):
    data = request.get_json()
    try:
        user = g.db.query(User).filter_by(id=user_id).first()
        if not user:
            return jsonify({"error": "User not found"}), 404

        new_car = Car(
            license_plate=data["number"],
            brand=data["brand"],
            model=data["model"],
            color=data["color"],
            owner_id=user_id,
        )
        g.db.add(new_car)
        g.db.commit()

        return jsonify(new_car.to_dict()), 201
    except Exception as e:
        g.db.rollback()
        return jsonify({"error": str(e)}), 500


## get user cars by id
@user_bp.route("/<string:user_id>/cars", methods=["GET"])
def get_user_cars(user_id):
    db: DbSessionType = cast(DbSessionType, g.db)
    try:
        user = db.query(User).filter_by(id=user_id).first()
        if not user:
            return jsonify({"error": "User not found"}), 404

        cars = [car.to_dict() for car in user.cars]
        return jsonify({"cars": cars}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


## patch user car by car id
@user_bp.route("/<string:user_id>/cars/<string:car_id>", methods=["PATCH"])
def patch_user_car(user_id, car_id):
    data = request.get_json()
    db: DbSessionType = cast(DbSessionType, g.db)
    if not data:
        return jsonify({"error": "No data provided"}), 400

    try:
        user = db.query(User).filter_by(id=user_id).first()
        if not user:
            return jsonify({"error": "User not found"}), 404

        car = db.query(Car).filter_by(id=car_id, owner_id=user_id).first()
        if not car:
            return jsonify({"error": "Car not found for this user"}), 404

        if "brand" in data:
            car.brand = data["brand"]
        if "model" in data:
            car.model = data["model"]
        if "number" in data:
            car.license_plate = data["number"]
        if "color" in data:
            car.color = data["color"]

        db.commit()
        return jsonify(car.to_dict()), 200

    except Exception as e:
        db.rollback()
        return jsonify({"error": str(e)}), 500


## Delete user car by car id
@user_bp.route("/<string:user_id>/cars/<string:car_id>", methods=["DELETE"])
def delete_user_car(user_id, car_id):
    db: DbSessionType = cast(DbSessionType, g.db)

    try:
        user = db.query(User).filter_by(id=user_id).first()
        if not user:
            return jsonify({"error": "User not found"}), 404

        car = db.query(Car).filter_by(id=car_id, owner_id=user_id).first()
        if not car:
            return jsonify({"error": "Car not found for this user"}), 404

        db.delete(car)
        db.commit()

        return jsonify({"status": "success", "message": f"Car {car_id} deleted"}), 204

    except Exception as e:
        db.rollback()
        return jsonify({"error": str(e)}), 500


## Get user bookings
@user_bp.route("/<string:user_id>/bookings", methods=["GET"])
def get_user_bookings(user_id):
    db: DbSessionType = cast(DbSessionType, g.db)
    try:
        user = db.query(User).filter_by(id=user_id).first()
        if not user:
            return jsonify({"error": "User not found"}), 404

        bookings = [booking.to_dict_extended() for booking in user.bookings]
        return jsonify({"bookings": bookings}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


## Get user transactions
@user_bp.route("/<string:user_id>/transactions", methods=["GET"])
def get_user_transactions(user_id):
    ## TODO Validate admin role
    db: DbSessionType = cast(DbSessionType, g.db)
    try:
        user = db.query(User).filter_by(id=user_id).first()
        if not user:
            return jsonify({"error": "User not found"}), 404

        transactions = [transaction.to_dict() for transaction in user.transactions]
        return jsonify({"transactions": transactions}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
