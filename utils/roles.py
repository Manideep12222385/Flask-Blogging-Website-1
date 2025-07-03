from functools import wraps
from flask import redirect, url_for, flash
from flask_login import current_user

def role_required(*roles):
    roles = [r.upper() for r in roles]

    def wrapper(fn):
        @wraps(fn)
        def decorated_view(*args, **kwargs):
            if not current_user.is_authenticated:
                flash("You must be logged in to access this page.", "warning")
                return redirect(url_for('auth.login'))

            if current_user.role.upper() not in roles:
                flash("You do not have permission to access this page.", "danger")
                return redirect(url_for('home.home'))

            return fn(*args, **kwargs)
        return decorated_view
    return wrapper
