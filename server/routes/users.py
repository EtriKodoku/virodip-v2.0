import requests
from flask import Blueprint, request, jsonify, g

from db.models import User, Car, Role, UserRole
from config.azure_config import azure_config
from config.logs_config import logger
from utils.graphAPI import create_b2c_user
from utils.roles import get_roles, register_roles

from typing import cast
from cast_types.g_types import DbSessionType

#   Add this line to every endpoint for enabling hints
#   db: DbSessionType = cast(DbSessionType, g.db)


user_bp = Blueprint("user_bp", __name__)


## Register user
@user_bp.route("/register", methods=["POST"], strict_slashes=False)
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
@user_bp.route("/", methods=["GET"], strict_slashes=False)
def get_users():
    db: DbSessionType = cast(DbSessionType, g.db)
    try:
        name = request.args.get("name")
        role = request.args.get("role")
        page = request.args.get("page", default=1, type=int)
        per_page = request.args.get("per_page", default=10, type=int)

        # Base query
        query = db.query(User)

        # Apply filters
        if name is not None:
            query = query.filter(User.name == name)

        if role is not None:
            query = query.join(UserRole, User.id == UserRole.user_id)\
                .join(Role, Role.id == UserRole.role_id)\
                .filter(Role.name == role)

        # Count after filters
        total = query.count()

        # Pagination math
        offset = (page - 1) * per_page

        # Apply pagination
        users = (
            query.order_by(User.id)
                .offset(offset)
                .limit(per_page)
                .all()
        )

        user_list = []

        for user in users:
            roles = (
                [role.name for role in user.roles]
                if hasattr(user, "roles")
                else get_roles(user.email)
            )
            user_data = user.to_dict()
            user_data["roles"] = roles
            user_list.append(user_data)

        result = {
            "users": user_list,
            "total": total,
            "page": page,
            "pages": (total + per_page - 1) // per_page,
            "has_next": offset + per_page < total,
            "has_prev": page > 1,
            "next_page": page + 1 if offset + per_page < total else None,
            "prev_page": page - 1 if page > 1 else None,
        }

        return jsonify(result), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


## Get user by ID
@user_bp.route("/<string:user_id>", methods=["GET"], strict_slashes=False)
def get_user(user_id):
    db: DbSessionType = cast(DbSessionType, g.db)
    try:
        user = db.query(User).filter_by(id=user_id).first()
        if not user:
            return jsonify({"error": "User not found"}), 404

        roles = (
            [role.name for role in user.roles]
            if hasattr(user, "roles")
            else get_roles(user.email)
        )

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
        page = request.args.get("page", default=1, type=int)
        per_page = request.args.get("per_page", default=10, type=int)
        query = db.query(Car).filter_by(owner_id=user_id)
        # Count after filters
        total = query.count()

        # Pagination math
        offset = (page - 1) * per_page

        # Apply pagination
        cars = (
            query.order_by(User.id)
                .offset(offset)
                .limit(per_page)
                .all()
        )
        result = {
            "cars": [car for car in cars],
            "total": total,
            "page": page,
            "pages": (total + per_page - 1) // per_page,
            "has_next": offset + per_page < total,
            "has_prev": page > 1,
            "next_page": page + 1 if offset + per_page < total else None,
            "prev_page": page - 1 if page > 1 else None,
        }
        return jsonify(result), 200

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
