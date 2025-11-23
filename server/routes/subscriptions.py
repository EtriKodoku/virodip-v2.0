from flask import Blueprint, request, g, jsonify, abort
from playhouse.shortcuts import model_to_dict
from db.models import UserSubscription
from config.logs_config import logger
from cast_types.g_types import DbSessionType

subscription_bp = Blueprint("subscription_bp", __name__)

##TODO FIX IT!!! db.connect is depreciated code. Use db.add and db.commit instead
## Add db: DbSessionType = g.db for hintings and proper code style


@subscription_bp.route("/subscriptions", methods=["POST"])
def create_subscription():
    data = request.get_json()
    db: DbSessionType = g.db
    if not data.get("plan"):
        return jsonify({"error": "plan is required"}), 400
    try:
        sub = UserSubscription.create(
            plan=data["plan"], active=data.get("active", True)
        )
        db.add(sub)
        db.commit()

        return jsonify(model_to_dict(sub)), 201

    except Exception as e:
        logger.error(f"Error while creating subscription: {e}")


@subscription_bp.route("/subscriptions", methods=["GET"])
def list_subscriptions():
    db.connect(reuse_if_open=True)
    try:
        subs = [model_to_dict(s) for s in UserSubscription.select()]
        return jsonify(subs)
    finally:
        db.close()


@subscription_bp.route("/subscriptions/<int:sub_id>", methods=["GET"])
def get_subscription(sub_id):
    db.connect(reuse_if_open=True)
    try:
        try:
            sub = UserSubscription.get(UserSubscription.id == sub_id)
        except UserSubscription.DoesNotExist:
            abort(404)
        return jsonify(model_to_dict(sub))
    finally:
        db.close()


@subscription_bp.route("/subscriptions/<int:sub_id>", methods=["PUT"])
def update_subscription(sub_id):
    data = request.get_json() or {}
    db.connect(reuse_if_open=True)
    try:
        try:
            sub = UserSubscription.get(UserSubscription.id == sub_id)
        except UserSubscription.DoesNotExist:
            abort(404)
        sub.plan = data.get("plan", sub.plan)
        sub.active = data.get("active", sub.active)
        sub.save()
        return jsonify(model_to_dict(sub))
    finally:
        db.close()


@subscription_bp.route("/subscriptions/<int:sub_id>", methods=["DELETE"])
def delete_subscription(sub_id):
    db.connect(reuse_if_open=True)
    try:
        try:
            sub = UserSubscription.get(UserSubscription.id == sub_id)
        except UserSubscription.DoesNotExist:
            abort(404)
        sub.delete_instance()
        return jsonify({"status": "deleted"})
    finally:
        db.close()
