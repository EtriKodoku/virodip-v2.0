import requests
from flask import Blueprint, request, jsonify, g
from db.models import User, SessionLocal  # Assuming Session = sessionmaker(bind=engine)
from config.azure_config import azure_config
from db.models import Booking, Parking, ParkingLot
from datetime import datetime


parking_bp = Blueprint("parking_bp", __name__)


## Get all parkings
@parking_bp.route("/", methods=["GET"])
def get_parkings():
    try:
        parkings = g.db.query(Parking).all()
        return jsonify([parking.to_dict() for parking in parkings]), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


## Get parking by ID
@parking_bp.route("/<int:parking_id>", methods=["GET"])
def get_parking(parking_id):
    try:
        parking = g.db.query(Parking).filter_by(id=parking_id).first()
        if not parking:
            return jsonify({"error": "Parking not found"}), 404
        return jsonify(parking.to_dict()), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


## add new parking
@parking_bp.route("/", methods=["POST"])
def create_parking():
    # if g.user.role != "admin":
    #     return jsonify({"error": "Forbidden"}), 403

    data = request.get_json()
    try:
        parking = Parking(
            name=data.get("name", "Default Parking"),
            location=data["location"],
            latitude=data["latitude"],
            longitude=data["longitude"],
            capacity=data["capacity"],
            available_spots=data[
                "available_spots"
            ],  # Initially, all spots are available
            created_at=datetime.utcnow(),
        )

        g.db.add(parking)
        g.db.commit()

        for _ in range(parking.capacity):
            parking_lot = ParkingLot(status="free", parking_id=parking.id)
            g.db.add(parking_lot)
            g.db.commit()

        return (
            jsonify(
                {
                    "id": parking.id,
                    "name": parking.name,
                    "location": parking.location,
                    "latitude": float(parking.latitude),
                    "longitude": float(parking.longitude),
                    "capacity": parking.capacity,
                    "created_at": parking.created_at.isoformat(),
                }
            ),
            201,
        )

    except Exception as e:
        g.db.rollback()
        return jsonify({"error": str(e)}), 500


# PATCH Parking
@parking_bp.route("/<string:parking_id>", methods=["PATCH"])
def update_parking(parking_id):
    # if g.user.role != "admin":
    #     return jsonify({"error": "Forbidden"}), 403

    data = request.get_json()
    parking_id = data.get("id")
    if not parking_id:
        return jsonify({"error": "id is required"}), 400

    try:
        parking = g.db.query(Parking).filter_by(id=parking_id).first()
        if not parking:
            return jsonify({"error": "Parking not found"}), 404

        if "name" in data:
            parking.name = data["name"]
        if "location" in data:
            parking.location = data["location"]
        if "latitude" in data:
            parking.latitude = data["latitude"]
        if "longitude" in data:
            parking.longitude = data["longitude"]
        if "capacity" in data:
            parking.capacity = data["capacity"]

        g.db.commit()
        return jsonify(parking.to_dict()), 200
    except Exception as e:
        g.db.rollback()
        return jsonify({"error": str(e)}), 500


# DELETE Parking
@parking_bp.route("/<string:parking_id>", methods=["DELETE"])
def delete_parking(parking_id):
    # if g.user.role != "admin":
    #     return jsonify({"error": "Forbidden"}), 403

    data = request.get_json()
    parking_id = data.get("id")
    if not parking_id:
        return jsonify({"error": "id is required"}), 400

    try:
        parking = g.db.query(Parking).filter_by(id=parking_id).first()
        if not parking:
            return jsonify({"error": "Parking not found"}), 404

        g.db.delete(parking)
        g.db.commit()
        return jsonify({"message": "Parking deleted"}), 200
    except Exception as e:
        g.db.rollback()
        return jsonify({"error": str(e)}), 500
