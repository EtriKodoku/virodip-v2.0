from flask import g
from config.config import manager_config
from db.models import User, Role, UserRole
from config.logs_config import logger

OWNER_EMAIL = manager_config.OWNER_EMAIL


def get_roles(email: str) -> str:
    if email == OWNER_EMAIL:
        return ["user", "analyst", "moderator", "admin", "owner"]
    return ["user"]


def register_roles(user, roles):
    logger.info(f"Registering roles for user {user.email}: {roles}")
    for role_name in roles:
        try:
            role = g.db.query(Role).filter_by(name=role_name).first()

            if not role:
                # Create new role if it doesn't exist
                role = Role(name=role_name)
                g.db.add(role)
                g.db.commit()
        except Exception as e:
            logger.error(f"Error while registering or creating roles: {e}")
            return "Failed"
        try:
            # Check if the user already has this role
            existing_user_role = (
                g.db.query(UserRole)
                .filter_by(user_id=user.id, role_id=role.id)
                .first()
            )
            if existing_user_role:
                logger.info(f"User {user.email} already has role [{role_name}], skipping assignment.")
                continue  # Skip adding if the role already exists for the user
        except Exception as e:
            logger.error(f"Error checking existing role: {e}")
            continue
        try:
            user_role = UserRole(user_id=user.id, role_id=role.id)
            g.db.add(user_role)
            g.db.commit()
            logger.info(f"Assigned role [{role_name}] to user {user.email}")
        except Exception as e:
            logger.error(f"Error while assigning role to user: {e}")
            g.db.rollback()
            continue
    
    return "Success"  ## TODO Change to proper logging


