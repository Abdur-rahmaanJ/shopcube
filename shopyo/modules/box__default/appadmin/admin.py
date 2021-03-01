from functools import wraps

from flask import flash
from flask import redirect
from flask import url_for

from flask_login import current_user

from init import login_manager
from shopyo.api.html import notify_warning

from modules.box__default.auth.models import User

login_manager.login_view = "auth.login"
login_manager.login_message = notify_warning("Please login for access")


@login_manager.user_loader
def load_user(id):
    return User.query.get(id)


def admin_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if current_user.is_admin:
            return f(*args, **kwargs)
        else:
            flash(notify_warning("You need to be an admin to view this page."))
            return redirect(url_for("dashboard.index"))

    return wrap
