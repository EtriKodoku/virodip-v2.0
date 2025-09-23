from flask import Blueprint, request, jsonify, abort
from playhouse.shortcuts import model_to_dict
from db.models import db, Car, User

car_bp = Blueprint('car_bp', __name__)

@car_bp.route('/cars', methods=['POST'])
def create_car():
    data = request.get_json() or {}
    if not data.get('owner_id') or not data.get('make') or not data.get('model'):
        return jsonify({'error': 'owner_id, make, and model are required'}), 400
    db.connect(reuse_if_open=True)
    try:
        try:
            owner = User.get(User.id == data['owner_id'])
        except User.DoesNotExist:
            abort(404)
        car = Car.create(owner=owner, make=data['make'], model=data['model'], year=data.get('year'))
        return jsonify(model_to_dict(car)), 201
    finally:
        db.close()

@car_bp.route('/cars', methods=['GET'])
def list_cars():
    db.connect(reuse_if_open=True)
    try:
        cars = [model_to_dict(c, backrefs=True) for c in Car.select()]
        return jsonify(cars)
    finally:
        db.close()

@car_bp.route('/cars/<int:car_id>', methods=['GET'])
def get_car(car_id):
    db.connect(reuse_if_open=True)
    try:
        try:
            car = Car.get(Car.id == car_id)
        except Car.DoesNotExist:
            abort(404)
        return jsonify(model_to_dict(car, backrefs=True))
    finally:
        db.close()

@car_bp.route('/cars/<int:car_id>', methods=['PUT'])
def update_car(car_id):
    data = request.get_json() or {}
    db.connect(reuse_if_open=True)
    try:
        try:
            car = Car.get(Car.id == car_id)
        except Car.DoesNotExist:
            abort(404)
        car.make = data.get('make', car.make)
        car.model = data.get('model', car.model)
        car.year = data.get('year', car.year)
        car.save()
        return jsonify(model_to_dict(car, backrefs=True))
    finally:
        db.close()

@car_bp.route('/cars/<int:car_id>', methods=['DELETE'])
def delete_car(car_id):
    db.connect(reuse_if_open=True)
    try:
        try:
            car = Car.get(Car.id == car_id)
        except Car.DoesNotExist:
            abort(404)
        car.delete_instance()
        return jsonify({'status': 'deleted'})
    finally:
        db.close()
