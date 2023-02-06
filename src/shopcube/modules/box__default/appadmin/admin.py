from functools import wraps

from flask import redirect
from flask_login import current_user
from init import login_manager
from modules.box__default.auth.models import User
from shopyo.api.html import notify_warning

login_manager.login_view = "auth.login"
# login_manager.login_message = "Please login for access"


@login_manager.user_loader
def load_user(id):
    return User.query.get(id)


def admin_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if current_user.is_admin:
            return f(*args, **kwargs)
        else:

            return redirect("/")

    return wrap
