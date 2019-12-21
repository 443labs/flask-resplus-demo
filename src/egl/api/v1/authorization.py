from flask_login import login_required, current_user
from functools import wraps
from werkzeug.exceptions import Unauthorized

from egl.db.models import Permission


def authorize(permission: Permission):
    """
    Requires the current user to be logged in (authenticted), as well as have the required permission assigned (authorized).
    """
    assert permission

    def decorator(f):
        @wraps(f)
        @login_required
        def wrapped(*args, **kwargs):
            if not current_user.has_permission(permission):
                raise Unauthorized("The current user requires the '{}' permission.".format(str(permission.name)))
            r = f(*args, **kwargs)
            return r
        return wrapped
    return decorator
