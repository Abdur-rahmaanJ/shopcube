from functools import wraps

from flask import redirect
from flask_login import current_user
from init import login_manager
from shopyo_auth.models import User
from shopyo.api.html import notify_warning




def admin_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if current_user.is_admin:
            return f(*args, **kwargs)
        else:

            return redirect("/")

    return wrap
