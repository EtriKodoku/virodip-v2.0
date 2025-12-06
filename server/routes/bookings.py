from datetime import datetime
from flask import Blueprint, request, jsonify, g
from sqlalchemy.orm import joinedload
from db.models import User, Booking, Parking
from cast_types.g_types import DbSessionType
from typing import cast
from auth.roles import hasRole

booking_bp = Blueprint("booking_bp", __name__)


SORT_MAP = {
    "start": Booking.start,
    "end": Booking.end,
    "created_at": Booking.created_at,
}


## Get bookings for a user
@booking_bp.route("/<user_id>", methods=["GET"])
def get_user_bookings(user_id):
    db: DbSessionType = cast(DbSessionType, g.db)
    try:
        parking_name = request.args.get("parking_name")
        status = request.args.get("status")
        page = request.args.get("page", default=1, type=int)
        per_page = request.args.get("per_page", default=10, type=int)
        sort = request.args.get("sort")   # e.g. "start", "-end"
        offset = (page - 1) * per_page

        query = db.query(Booking).filter_by(user_id=user_id)

        if parking_name:
            query = (
                query
                .join(Parking, Booking.parking_id == Parking.id)
                .filter(Parking.name.ilike(f"%{parking_name}%"))
            )

        if status:
            query = query.filter(Booking.status == status)

        total = query.count()

        if sort:
            direction = sort.startswith("-")
            key = sort.lstrip("-")

            if key in SORT_MAP:
                column = SORT_MAP[key]
                query = query.order_by(column.desc() if direction else column.asc())
        else:
            # default sorting by created_at DESC
            query = query.order_by(Booking.created_at.desc())

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


@booking_bp.route("/", methods=["GET"])
# @hasRole("admin")  # enable later
def get_all_bookings():
    try:
        db = g.db

        # Query params
        user_id = request.args.get("userId", type=str)
        parking_id = request.args.get("parkingId", type=str)
        parking_name = request.args.get("parkingName")
        status = request.args.get("status")

        start_from = request.args.get("start_from")
        start_to = request.args.get("start_to")
        end_from = request.args.get("end_from")
        end_to = request.args.get("end_to")

        page = request.args.get("page", default=1, type=int)
        per_page = request.args.get("per_page", default=10, type=int)
        offset = (page - 1) * per_page

        sort = request.args.get("sort")

        query = (
            db.query(Booking)
            .options(
                joinedload(Booking.user),
                joinedload(Booking.car),
                joinedload(Booking.parking)
            )
        )

        # START of filters
        if user_id:
            query = query.filter(Booking.user_id == user_id)

        if parking_id:
            query = query.filter(Booking.parking_id == parking_id)

        if parking_name:
            query = query.join(Booking.parking).filter(
                Parking.name.ilike(f"%{parking_name}%")
            )

        if status:
            query = query.filter(Booking.status == status)

        if start_from:
            query = query.filter(Booking.start >= start_from)
        if start_to:
            query = query.filter(Booking.start <= start_to)

        if end_from:
            query = query.filter(Booking.end >= end_from)
        if end_to:
            query = query.filter(Booking.end <= end_to)
        ## END of filters

        total = query.count()

        if sort:
            direction = sort.startswith("-")
            key = sort.lstrip("-")

            if key in SORT_MAP:
                column = SORT_MAP[key]
                query = query.order_by(column.desc() if direction else column.asc())
        else:
            query = query.order_by(Booking.created_at.asc())

        # Pagination
        bookings = (
            query.offset(offset)
                 .limit(per_page)
                 .all()
        )

        # Serialize
        result = {
            "bookings": [b.to_dict_extended() for b in bookings],
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
