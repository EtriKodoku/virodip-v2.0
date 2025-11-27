from functools import wraps
from typing import Iterable, List, Optional, Union
from flask import g, request, jsonify

from db.models import User


def _parse_roles_from_token(token_data) -> List[str]:
    """Parse roles from token data returned by Azure B2C (or similar).

    This project stores roles in the `extension_Role` claim as a comma-separated
    string (see logs). We try several common claim names for robustness.
    """
    if not token_data:
        return []

    # Common claim names used in this project/logs
    for claim in ("extension_Role", "roles", "role", "roles_claim"):
        val = token_data.get(claim) if isinstance(token_data, dict) else None
        if not val:
            continue
        if isinstance(val, str):
            return [r.strip() for r in val.split(",") if r.strip()]
        if isinstance(val, (list, tuple)):
            return [str(r).strip() for r in val if str(r).strip()]

    return []


def _load_roles_from_db(db_session, user_id: str) -> List[str]:
    """Load roles for a user from the database using the provided session.

    Returns list of role names (strings). If the user is not found, returns [].
    """
    if not db_session or not user_id:
        return []
    try:
        user = db_session.query(User).filter_by(id=user_id).first()
        if not user:
            return []
        return user.get_roles()
    except Exception:
        return []


def get_request_roles() -> List[str]:
    """Return roles for the current request.

    Priority:
    - If `g._roles_cache` set, return it.
    - If `g.user` exists and has `get_roles`, use DB to load roles (via relationship).
    - If `request.environ['token_data']` exists, parse roles from token claims.
    - Otherwise return [].
    """
    if hasattr(g, "_roles_cache") and isinstance(g._roles_cache, list):
        return g._roles_cache

    roles: List[str] = []

    # If g.user is populated with ORM User instance, prefer DB-backed roles
    user_obj = getattr(g, "user", None)
    if user_obj is not None:
        # If it's an ORM instance with get_roles method, use it
        if hasattr(user_obj, "get_roles"):
            try:
                roles = user_obj.get_roles()
            except Exception:
                roles = []
        else:
            # If it's a mapping (e.g., token data), try parse
            try:
                roles = _parse_roles_from_token(user_obj)
            except Exception:
                roles = []

    # If still empty, check token_data from environ (middleware may set it)
    if not roles:
        token_data = request.environ.get("token_data") or getattr(g, "token_data", None)
        roles = _parse_roles_from_token(token_data)

    # Cache for request lifetime
    g._roles_cache = roles
    return roles


def hasRole(required: Union[str, Iterable[str]], require_all: bool = False):
    """Decorator to require one or more roles for a Flask route.

    Usage examples:
        @hasRole('admin')
        @hasRole(['admin', 'manager'])               # any of
        @hasRole(['roleA','roleB'], require_all=True)  # require all

    Behavior:
    - If no authenticated user / token present -> returns 401.
    - If user lacks required role(s) -> returns 403.
    - Otherwise proceeds to the route function.
    """

    if isinstance(required, str):
        required_roles = [required]
    else:
        required_roles = [str(r) for r in required]

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # If no DB/session or token at all, return 401
            # Check for authentication evidence
            auth_user = getattr(g, "user", None)
            token_data = request.environ.get("token_data") or getattr(g, "token_data", None)
            if auth_user is None and token_data is None:
                return jsonify({"error": "Unauthorized"}), 401

            roles = get_request_roles()

            if require_all:
                ok = all(r in roles for r in required_roles)
            else:
                ok = any(r in roles for r in required_roles)

            if not ok:
                return jsonify({"error": "Forbidden"}), 403

            return func(*args, **kwargs)

        return wrapper

    return decorator
