from config.config import manager_config
from db.models import User, Role, UserRole

OWNER_EMAIL = manager_config.OWNER_EMAIL


def get_roles(email: str) -> str:
    if email == OWNER_EMAIL:
        return ["user", "analyst", "moderator", "admin", "owner"]
    return ["user"]


def register_roles(user, roles):
    try:
        for role in roles:
            role_obj, created = Role.get_or_create(name=role)
            UserRole.get_or_create(user=user, role=role_obj)
        return "Success"  ## TODO Change to proper logging
    except Exception as e:
        print(f"Error registering roles: {e}")
        return "Failed"
