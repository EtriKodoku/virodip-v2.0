from flask import Blueprint, request, jsonify, g
from db.models import Device
from typing import cast
from cast_types.g_types import DbSessionType

device_bp = Blueprint("device_bp", __name__)

#   Add this line to every endpoint for enabling hints
#   db: DbSessionType = cast(DbSessionType, g.db)


@device_bp.route("/", methods=["POST"])
def create_device():
    db: DbSessionType = cast(DbSessionType, g.db)
    try:
        data = request.get_json()
        serial_number = data.get("serial_number")
        token = data.get("token")
        parking_id = data.get("parking_id")

        if not serial_number or not token:
            return jsonify({"error": "Missing serial_number or token"}), 400

        existing = db.query(Device).filter_by(serial_number=serial_number).first()
        if existing:
            return (
                jsonify({"error": "Device with this serial number already exists"}),
                409,
            )

        new_device = Device(
            serial_number=serial_number,
            token=token,
            status="pending",
            issued=False,
            parking_id=parking_id,
        )
        db.add(new_device)
        db.commit()

        return jsonify(new_device.to_dict()), 201

    except Exception as e:
        db.rollback()
        return jsonify({"error": str(e)}), 500


@device_bp.route("/<string:serial_number>", methods=["GET"])
def get_device(serial_number):
    db: DbSessionType = cast(DbSessionType, g.db)
    try:
        device = db.query(Device).filter_by(serial_number=serial_number).first()
        if not device:
            return jsonify({"error": "Device not found"}), 404

        return jsonify(device.to_dict()), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@device_bp.route("/", methods=["GET"])
def list_devices():
    db: DbSessionType = cast(DbSessionType, g.db)
    try:
        devices = db.query(Device).all()
        result = [d.to_dict() for d in devices]
        return jsonify(result), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@device_bp.route("/<string:serial_number>", methods=["PUT"])
def update_device(serial_number):
    db: DbSessionType = cast(DbSessionType, g.db)
    try:
        device = db.query(Device).filter_by(serial_number=serial_number).first()
        if not device:
            return jsonify({"error": "Device not found"}), 404

        data = request.get_json()
        if "token" in data:
            device.token = data["token"]
        if "status" in data:
            device.status = data["status"]
        if "issued" in data:
            device.issued = data["issued"]
        if "parking_id" in data:
            device.parking_id = data["parking_id"]

        db.commit()
        return jsonify(device.to_dict()), 200

    except Exception as e:
        db.rollback()
        return jsonify({"error": str(e)}), 500


@device_bp.route("/<string:serial_number>", methods=["DELETE"])
def delete_device(serial_number):
    db: DbSessionType = cast(DbSessionType, g.db)
    try:
        device = db.query(Device).filter_by(serial_number=serial_number).first()
        if not device:
            return jsonify({"error": "Device not found"}), 404

        db.delete(device)
        db.commit()
        return jsonify({"status": "deleted"}), 200

    except Exception as e:
        db.rollback()
        return jsonify({"error": str(e)}), 500
