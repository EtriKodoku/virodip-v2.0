import requests
from flask import Blueprint, request, jsonify, g
from db.models import User, SessionLocal  # Assuming Session = sessionmaker(bind=engine)
from config.azure_config import azure_config
from db.models import Booking, Parking
from datetime import datetime

booking_bp = Blueprint("booking_bp", __name__)


## Get bookings for a user
@booking_bp.route("/<user_id>", methods=["GET"])
def get_user_bookings(user_id):
    try:
        user = g.db.query(User).filter_by(id=user_id).first()
        if not user:
            return jsonify({"error": "User not found"}), 404

        bookings = [
            booking.to_dict() for booking in user.bookings
        ]  # Assuming a to_dict method exists
        return jsonify({"booking": bookings}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


## Get all bookings
@booking_bp.route("/", methods=["GET"])
def get_all_bookings():
    try:
        bookings = g.db.query(Booking).all()
        return jsonify([booking.to_dict() for booking in bookings]), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


## Create a new booking
@booking_bp.route("/", methods=["POST"])
def create_booking():
    data = request.get_json()
    try:
        if not data:
            return jsonify({"error": "No data provided"}), 400
        user_id = data.get("userId")  # or g.user.id

        parking = g.db.query(Parking).filter_by(id=data["parkingId"]).first()
        parking.update_available_spots()
        if not parking:
            return jsonify({"error": "Parking not found"}), 404
        if parking.available_spots <= 0:
            return jsonify({"error": "No available spots"}), 400

        parking.available_spots -= 1

        new_booking = Booking(
            user_id=user_id,
            parking_id=data["parkingId"],
            car_id=data["carId"],
            # date=datetime.strptime(data["date"], "%Y-%m-%d").date(),
            start=datetime.strptime(data["start"], "%Y-%m-%d %H:%M"),
            end=datetime.strptime(data["end"], "%Y-%m-%d %H:%M"),
            status="active",
        )

        g.db.add(new_booking)
        g.db.commit()

        ##TODO Calculate price and create transaction if needed

        return jsonify(new_booking.to_dict()), 201

    except Exception as e:
        g.db.rollback()
        return jsonify({"error": str(e)}), 500


## Patch booking
@booking_bp.route("/<string:booking_id>", methods=["PATCH"])
def update_booking(booking_id):
    data = request.get_json()
    booking_id = data.get("id")
    if not booking_id:
        return jsonify({"error": "id is required"}), 400

    try:
        booking = g.db.query(Booking).filter_by(id=booking_id).first()
        if not booking:
            return jsonify({"error": "Booking not found"}), 404

        # Update fields
        if "status" in data:
            old_status = booking.status
            booking.status = data["status"]

            # Handle cancellation: return spot
            if data["status"] == "cancelled" and old_status != "cancelled":
                parking = g.db.query(Parking).filter_by(id=booking.parking_id).first()
                if parking:
                    parking.capacity += 1

        if "start" in data:
            booking.start_time = data["start"]
        if "end" in data:
            booking.end_time = data["end"]

        g.db.commit()
        return jsonify(booking.to_dict()), 200
    except Exception as e:
        g.db.rollback()
        return jsonify({"error": str(e)}), 500


# DELETE Booking
@booking_bp.route("/<string:booking_id>", methods=["DELETE"])
def delete_booking(booking_id):
    if not booking_id:
        return jsonify({"error": "id is required"}), 400

    try:
        booking = g.db.query(Booking).filter_by(id=booking_id).first()
        if not booking:
            return jsonify({"error": "Booking not found"}), 404

        g.db.delete(booking)
        g.db.commit()
        return "", 204  # No Content
    except Exception as e:
        g.db.rollback()
        return jsonify({"error": str(e)}), 500
