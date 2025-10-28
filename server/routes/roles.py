from flask import Blueprint, request, jsonify, abort
from playhouse.shortcuts import model_to_dict
from db.models import db, Role

role_bp = Blueprint("role_bp", __name__)


@role_bp.route("/roles", methods=["POST"])
def create_role():
    data = request.get_json() or {}
    if not data.get("name"):
        return jsonify({"error": "name is required"}), 400
    db.connect(reuse_if_open=True)
    try:
        role = Role.create(name=data["name"])
        return jsonify(model_to_dict(role)), 201
    finally:
        db.close()


@role_bp.route("/roles", methods=["GET"])
def list_roles():
    db.connect(reuse_if_open=True)
    try:
        roles = [model_to_dict(r) for r in Role.select()]
        return jsonify(roles)
    finally:
        db.close()


@role_bp.route("/roles/<int:role_id>", methods=["GET"])
def get_role(role_id):
    db.connect(reuse_if_open=True)
    try:
        try:
            role = Role.get(Role.id == role_id)
        except Role.DoesNotExist:
            abort(404)
        return jsonify(model_to_dict(role))
    finally:
        db.close()


@role_bp.route("/roles/<int:role_id>", methods=["PUT"])
def update_role(role_id):
    data = request.get_json() or {}
    db.connect(reuse_if_open=True)
    try:
        try:
            role = Role.get(Role.id == role_id)
        except Role.DoesNotExist:
            abort(404)
        role.name = data.get("name", role.name)
        role.save()
        return jsonify(model_to_dict(role))
    finally:
        db.close()


@role_bp.route("/roles/<int:role_id>", methods=["DELETE"])
def delete_role(role_id):
    db.connect(reuse_if_open=True)
    try:
        try:
            role = Role.get(Role.id == role_id)
        except Role.DoesNotExist:
            abort(404)
        role.delete_instance()
        return jsonify({"status": "deleted"})
    finally:
        db.close()
