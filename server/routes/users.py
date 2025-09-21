from flask import Blueprint, request, jsonify, abort
from playhouse.shortcuts import model_to_dict
from models import db, User, Role, UserSubscription, Car, Transaction, UserRole
from playhouse.shortcuts import model_to_dict
import uuid

user_bp = Blueprint('user_bp', __name__)


@user_bp.route('/users', methods=['POST'])
def create_user():
	data = request.get_json() or {}
	if not data.get('name') or not data.get('email'):
		return jsonify({'error': 'name and email are required'}), 400

	user_id = data.get('id') or str(uuid.uuid4())
	db.connect_db()
	try:
		subscription = None
		if data.get('subscription'):
			sub = data['subscription']
			subscription = UserSubscription.create(plan=sub.get('plan', 'free'), active=sub.get('active', True))

		user = User.create(
			id=user_id,
			name=data.get('name'),
			email=data.get('email'),
			phone_number=data.get('phoneNumber'),
			avatar_url=data.get('avatarUrl'),
			subscription=subscription,
		)

		for r in data.get('roles', []):
			role_obj, _ = Role.get_or_create(name=r.get('name') if isinstance(r, dict) else r)
			UserRole.create(user=user, role=role_obj)

		for c in data.get('cars', []):
			Car.create(owner=user, make=c.get('make'), model=c.get('model'), year=c.get('year'))

		return jsonify(model_to_dict(user, backrefs=True, recurse=False)), 201
	finally:
		db.close_db()


@user_bp.route('/users', methods=['GET'])
def list_users():
	db.connect_db()
	try:
		users = [model_to_dict(u, backrefs=True) for u in User.select()]
		return jsonify(users)
	finally:
		db.close_db()


@user_bp.route('/users/<user_id>', methods=['GET'])
def get_user(user_id):
	db.connect_db()
	try:
		try:
			user = User.get(User.id == user_id)
		except User.DoesNotExist:
			abort(404)
		return jsonify(model_to_dict(user, backrefs=True))
	finally:
		db.close_db()


@user_bp.route('/users/<user_id>', methods=['PUT'])
def update_user(user_id):
	data = request.get_json() or {}
	db.connect_db()
	try:
		try:
			user = User.get(User.id == user_id)
		except User.DoesNotExist:
			abort(404)

		user.name = data.get('name', user.name)
		user.email = data.get('email', user.email)
		user.phone_number = data.get('phoneNumber', user.phone_number)
		user.avatar_url = data.get('avatarUrl', user.avatar_url)
		user.save()

		if 'roles' in data:
			UserRole.delete().where(UserRole.user == user).execute()
			for r in data.get('roles', []):
				role_obj, _ = Role.get_or_create(name=r.get('name') if isinstance(r, dict) else r)
				UserRole.create(user=user, role=role_obj)

		return jsonify(model_to_dict(user, backrefs=True))
	finally:
		db.close_db()


@user_bp.route('/users/<user_id>', methods=['DELETE'])
def delete_user(user_id):
	db.connect_db()
	try:
		try:
			user = User.get(User.id == user_id)
		except User.DoesNotExist:
			abort(404)

		# cascade delete related objects manually
		Car.delete().where(Car.owner == user).execute()
		Transaction.delete().where(Transaction.user == user).execute()
		UserRole.delete().where(UserRole.user == user).execute()
		if user.subscription:
			user.subscription.delete_instance()
		user.delete_instance()

		return jsonify({'status': 'deleted'})
	finally:
		db.close_db()