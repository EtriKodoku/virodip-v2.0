from flask import Blueprint, request, jsonify, abort
from playhouse.shortcuts import model_to_dict
from db.models import db, UserRole, User, Role

userrole_bp = Blueprint("userrole_bp", __name__)

# Константи ролей — краще зберігати в таблиці, але для логіки підходить і так
ROLE_OWNER = "owner"
ROLE_ADMIN = "admin"
ROLE_GUARD = "guard"

def get_user_roles(user):
    return {ur.role.name for ur in UserRole.select().where(UserRole.user == user)}


def can_assign(current_user_roles, role_name):
    # Власника не може встановити ніхто
    if role_name == ROLE_OWNER:
        return False

    # Власник може ставити адмінів і охоронців
    if ROLE_OWNER in current_user_roles:
        return True

    # Адмін може ставити лише охоронця
    if ROLE_ADMIN in current_user_roles and role_name == ROLE_GUARD:
        return True

    return False


@userrole_bp.route("/userroles/<int:user_id>", methods=["PUT"])
def set_user_roles(user_id):
    data = request.get_json() or {}
    role_ids = data.get("role_ids")

    if not isinstance(role_ids, list):
        return jsonify({"error": "role_ids must be a list"}), 400

    # Поточний користувач (хто робить запит)
    # Тут встав свій метод отримання current_user
    current_user = request.current_user
    current_roles = get_user_roles(current_user)

    db.connect(reuse_if_open=True)
    try:
        try:
            target_user = User.get(User.id == user_id)
        except User.DoesNotExist:
            abort(404)

        # Завантажуємо всі ролі
        roles = list(Role.select().where(Role.id.in_(role_ids)))
        if len(roles) != len(role_ids):
            return jsonify({"error": "One or more roles not found"}), 400

        # Перевіряємо правила ACL
        for role in roles:
            if not can_assign(current_roles, role.name):
                return jsonify({
                    "error": f"You cannot assign role '{role.name}'"
                }), 403

        # Перезаписуємо ролі цілком
        UserRole.delete().where(UserRole.user == target_user).execute()

        for r in roles:
            UserRole.create(user=target_user, role=r)

        # Відповідь з новими ролями
        new_roles = [
            model_to_dict(ur, backrefs=True)
            for ur in UserRole.select().where(UserRole.user == target_user)
        ]

        return jsonify({
            "user_id": user_id,
            "roles": new_roles
        }), 200

    finally:
        db.close()
