from flask import redirect
from flask import url_for
from flask_login import current_user
from functools import wraps


def check_confirmed(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if current_user.is_email_confirmed:
            return func(*args, **kwargs)
        return redirect(url_for("auth.unconfirmed"))

    return decorated_function
