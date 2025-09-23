from flask import Blueprint, request, jsonify, abort
from playhouse.shortcuts import model_to_dict
from db.models import db, UserRole, User, Role

userrole_bp = Blueprint('userrole_bp', __name__)

@userrole_bp.route('/userroles', methods=['POST'])
def create_userrole():
    data = request.get_json() or {}
    if not data.get('user_id') or not data.get('role_id'):
        return jsonify({'error': 'user_id and role_id are required'}), 400
    db.connect(reuse_if_open=True)
    try:
        try:
            user = User.get(User.id == data['user_id'])
            role = Role.get(Role.id == data['role_id'])
        except (User.DoesNotExist, Role.DoesNotExist):
            abort(404)
        ur = UserRole.create(user=user, role=role)
        return jsonify(model_to_dict(ur)), 201
    finally:
        db.close()

@userrole_bp.route('/userroles', methods=['GET'])
def list_userroles():
    db.connect(reuse_if_open=True)
    try:
        urs = [model_to_dict(ur, backrefs=True) for ur in UserRole.select()]
        return jsonify(urs)
    finally:
        db.close()

@userrole_bp.route('/userroles/<int:ur_id>', methods=['GET'])
def get_userrole(ur_id):
    db.connect(reuse_if_open=True)
    try:
        try:
            ur = UserRole.get(UserRole.id == ur_id)
        except UserRole.DoesNotExist:
            abort(404)
        return jsonify(model_to_dict(ur, backrefs=True))
    finally:
        db.close()

@userrole_bp.route('/userroles/<int:ur_id>', methods=['PUT'])
def update_userrole(ur_id):
    data = request.get_json() or {}
    db.connect(reuse_if_open=True)
    try:
        try:
            ur = UserRole.get(UserRole.id == ur_id)
        except UserRole.DoesNotExist:
            abort(404)
        if data.get('user_id'):
            try:
                user = User.get(User.id == data['user_id'])
                ur.user = user
            except User.DoesNotExist:
                abort(404)
        if data.get('role_id'):
            try:
                role = Role.get(Role.id == data['role_id'])
                ur.role = role
            except Role.DoesNotExist:
                abort(404)
        ur.save()
        return jsonify(model_to_dict(ur, backrefs=True))
    finally:
        db.close()

@userrole_bp.route('/userroles/<int:ur_id>', methods=['DELETE'])
def delete_userrole(ur_id):
    db.connect(reuse_if_open=True)
    try:
        try:
            ur = UserRole.get(UserRole.id == ur_id)
        except UserRole.DoesNotExist:
            abort(404)
        ur.delete_instance()
        return jsonify({'status': 'deleted'})
    finally:
        db.close()
