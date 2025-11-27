from datetime import datetime
from flask import Blueprint, request, jsonify, g
from db.models import User, Booking, Parking
from cast_types.g_types import DbSessionType
from typing import cast
from auth.roles import hasRole

booking_bp = Blueprint("booking_bp", __name__)


## Get bookings for a user
@booking_bp.route("/<user_id>", methods=["GET"])
def get_user_bookings(user_id):
    db: DbSessionType = cast(DbSessionType, g.db)
    try:
        parking_name = request.args.get("parking_name")
        status = request.args.get("status")
        page = request.args.get("page", default=1, type=int)
        per_page = request.args.get("per_page", default=10, type=int)
        offset = (page - 1) * per_page

        query = db.query(Booking).filter_by(user_id=user_id)

        # Filter by parking name (contains)
        if parking_name:
            query = (
                query
                .join(Parking, Booking.parking_id == Parking.id)
                .filter(Parking.name.ilike(f"%{parking_name}%"))
            )

        # Filter by status
        if status:
            query = query.filter(Booking.status == status)

        total = query.count()

        bookings = (
            query
            .offset(offset)
            .limit(per_page)
            .all()
        )

        result = {
            "bookings": [booking.to_dict_extended() for booking in bookings],
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


## Get all bookings
@booking_bp.route("/", methods=["GET"])
# @hasRole("user")  ## TODO Enable role check
def get_all_bookings():
    try:
        user_id = request.args.get("userId", type=int)
        page = request.args.get("page", default=1, type=int)
        per_page = request.args.get("per_page", default=10, type=int)
        offset = (page - 1) * per_page

        # Start query
        query = g.db.query(Booking)

        # Filter by user_id if provided
        if user_id is not None:
            query = query.filter(Booking.user_id == user_id)

        # Count AFTER filters
        total = query.count()

        # Apply pagination
        bookings = (
            query
            .order_by(Booking.id)
            .offset(offset)
            .limit(per_page)
            .all()
        )

        result = {
            "bookings": [booking.to_dict_extended() for booking in bookings],
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
            start=datetime.strptime(data["start"], "%Y-%m-%dT%H:%M"),
            end=datetime.strptime(data["end"], "%Y-%m-%dT%H:%M"),
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
                    parking.available_spots += 1

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


@booking_bp.route("/test", methods=["POST"])
def test_booking():

    data = request.get_json()
    print(data["start"])
    start = (datetime.strptime(data["start"], "%Y-%m-%dT%H:%M"),)
    end = (datetime.strptime(data["end"], "%Y-%m-%dT%H:%M"),)
    print(type(start))
    return jsonify({"start": start, "end": end})
