from flask import g
from config.config import manager_config
from db.models import User, Role, UserRole

OWNER_EMAIL = manager_config.OWNER_EMAIL


def get_roles(email: str) -> str:
    if email == OWNER_EMAIL:
        return ["user", "analyst", "moderator", "admin", "owner"]
    return ["user"]


def register_roles(user, roles):
    try:
        for role_name in roles:
            role = g.db.query(Role).filter_by(name=role_name).first()

            if not role:
                # Create new role if it doesn't exist
                role = Role(name=role_name)
                g.db.add(role)
                g.db.commit()

            user_role = UserRole(user_id=user.id, role_id=role.id)
            g.db.add(user_role)
            g.db.commit()
        return "Success"  ## TODO Change to proper logging
    except Exception as e:
        print(f"Error registering roles: {e}")
        return "Failed"
