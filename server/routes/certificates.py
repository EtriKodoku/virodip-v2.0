import os
from datetime import datetime
from flask import Blueprint, request, jsonify, g

from config.logs_config import logger
from config.config import ca_config
from db.models import Device
from utils.CA_sign import sign_csr, generate_crl

from typing import cast
from cast_types.g_types import DbSessionType

#   Add this line to every endpoint for enabling hints
#   db: DbSessionType = cast(DbSessionType, g.db)

certificates_bp = Blueprint("certificates_bp", __name__)


@certificates_bp.post("/provision")
def provision():
    db: DbSessionType = cast(DbSessionType, g.db)

    data = request.json
    csr_pem = data.get("csr")
    serial = data.get("serial")
    token = data.get("token")

    if not csr_pem or not serial or not token:
        return jsonify({"error": "Missing fields"}), 400

    device = db.query(Device).filter_by(serial_number=serial).first()
    if not device or device.token != token or device.issued:
        return jsonify({"error": "Unauthorized or already provisioned"}), 403

    cert_pem, cert = sign_csr(csr_pem, serial)

    device.cert_serial = str(cert.get_serial_number())
    device.issued = True
    device.status = "active"
    device.issued_at = datetime.now()
    db.commit()

    return jsonify({"certificate": cert_pem.decode()})


@certificates_bp.post("/renew")
def renew():
    db: DbSessionType = cast(DbSessionType, g.db)

    data = request.json
    csr_pem = data.get("csr")
    serial = data.get("serial")

    device = db.query(Device).filter_by(serial_number=serial, status="active").first()
    if not device:
        return jsonify({"error": "Unknown or inactive device"}), 404

    cert_pem, cert = sign_csr(csr_pem, serial)
    device.cert_serial = str(cert.get_serial_number())
    device.renewed_at = datetime.now()
    db.add()
    db.commit()

    return jsonify({"certificate": cert_pem.decode()})


@certificates_bp.post("/revoke")
def revoke():
    db: DbSessionType = cast(DbSessionType, g.db)

    data = request.json
    serial = data.get("serial")

    device = db.query(Device).filter_by(serial_number=serial).first()
    if not device:
        return jsonify({"error": "Unknown device"}), 404

    device.status = "revoked"
    device.revoked_at = datetime.now()
    db.session.commit()
    generate_crl(db)

    return jsonify({"status": "revoked"})


@certificates_bp.get("/crl")
def get_crl():
    """Get Certificate Revocation List"""
    db: DbSessionType = cast(DbSessionType, g.db)

    CRL_FILE = ca_config.CRL_FILE
    if not os.path.exists(CRL_FILE):
        generate_crl(db)
    with open(CRL_FILE, "r") as f:
        return f.read(), 200, {"Content-Type": "application/x-pem-file"}
