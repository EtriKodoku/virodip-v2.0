from flask import Blueprint, request, jsonify, abort
from playhouse.shortcuts import model_to_dict
from models import db, Transaction, User

transaction_bp = Blueprint('transaction_bp', __name__)

@transaction_bp.route('/transactions', methods=['POST'])
def create_transaction():
    data = request.get_json() or {}
    if not data.get('user_id') or not data.get('amount'):
        return jsonify({'error': 'user_id and amount are required'}), 400
    db.connect(reuse_if_open=True)
    try:
        try:
            user = User.get(User.id == data['user_id'])
        except User.DoesNotExist:
            abort(404)
        txn = Transaction.create(user=user, amount=data['amount'], description=data.get('description'))
        return jsonify(model_to_dict(txn)), 201
    finally:
        db.close()

@transaction_bp.route('/transactions', methods=['GET'])
def list_transactions():
    db.connect(reuse_if_open=True)
    try:
        txns = [model_to_dict(t, backrefs=True) for t in Transaction.select()]
        return jsonify(txns)
    finally:
        db.close()

@transaction_bp.route('/transactions/<int:txn_id>', methods=['GET'])
def get_transaction(txn_id):
    db.connect(reuse_if_open=True)
    try:
        try:
            txn = Transaction.get(Transaction.id == txn_id)
        except Transaction.DoesNotExist:
            abort(404)
        return jsonify(model_to_dict(txn, backrefs=True))
    finally:
        db.close()

@transaction_bp.route('/transactions/<int:txn_id>', methods=['PUT'])
def update_transaction(txn_id):
    data = request.get_json() or {}
    db.connect(reuse_if_open=True)
    try:
        try:
            txn = Transaction.get(Transaction.id == txn_id)
        except Transaction.DoesNotExist:
            abort(404)
        txn.amount = data.get('amount', txn.amount)
        txn.description = data.get('description', txn.description)
        txn.save()
        return jsonify(model_to_dict(txn, backrefs=True))
    finally:
        db.close()

@transaction_bp.route('/transactions/<int:txn_id>', methods=['DELETE'])
def delete_transaction(txn_id):
    db.connect(reuse_if_open=True)
    try:
        try:
            txn = Transaction.get(Transaction.id == txn_id)
        except Transaction.DoesNotExist:
            abort(404)
        txn.delete_instance()
        return jsonify({'status': 'deleted'})
    finally:
        db.close()
