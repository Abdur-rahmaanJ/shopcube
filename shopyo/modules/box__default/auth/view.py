import json
import os
import datetime
from flask import Blueprint
from flask import flash
from flask import redirect
from flask import render_template
from flask import url_for
from flask import current_app
from flask import request
from flask_login import current_user
from flask_login import login_required
from flask_login import login_user
from flask_login import logout_user
from sqlalchemy import func

from shopyo.api.html import notify_danger
from shopyo.api.html import notify_success
from shopyo.api.html import notify_warning
from shopyo.api.security import get_safe_redirect

from .models import User
from .email import send_async_email
from .forms import LoginForm
from .forms import RegistrationForm


dirpath = os.path.dirname(os.path.abspath(__file__))
module_info = {}

with open(dirpath + "/info.json") as f:
    module_info = json.load(f)

auth_blueprint = Blueprint(
    "auth",
    __name__,
    url_prefix=module_info["url_prefix"],
    template_folder="templates",
)


@auth_blueprint.route("/register", methods=["GET", "POST"])
def register():

    context = {}
    reg_form = RegistrationForm()

    if reg_form.validate_on_submit():
        email = reg_form.email.data
        password = reg_form.password.data
        user = User.create(email=email, password=password)
        login_user(user)

        is_disabled = False

        if "EMAIL_CONFIRMATION_DISABLED" in current_app.config:
            is_disabled = current_app.config["EMAIL_CONFIRMATION_DISABLED"]

        if is_disabled is True:
            user.is_email_confirmed = True
            user.email_confirm_date = datetime.datetime.now()
            user.update()
        else:
            token = user.generate_confirmation_token()
            template = "auth/emails/activate_user"
            subject = "Please confirm your email"
            context.update({"token": token, "user": user})
            send_async_email(email, subject, template, **context)
            flash(
                notify_success("A confirmation email has been sent via email.")
            )

        return redirect(url_for("dashboard.index"))

    context["form"] = reg_form
    return render_template("auth/register.html", **context)


@auth_blueprint.route("/confirm/<token>")
@login_required
def confirm(token):

    if current_user.is_email_confirmed:
        flash(notify_warning("Account already confirmed."))
        return redirect(url_for("dashboard.index"))

    if current_user.confirm_token(token):
        flash(notify_success("You have confirmed your account. Thanks!"))
        return redirect(url_for("dashboard.index"))

    flash(notify_warning("The confirmation link is invalid/expired."))
    return redirect(url_for("auth.unconfirmed"))


@auth_blueprint.route("/resend")
@login_required
def resend():

    if current_user.is_email_confirmed:
        return redirect(url_for("dashboard.index"))

    token = current_user.generate_confirmation_token()
    template = "auth/emails/activate_user"
    subject = "Please confirm your email"
    context = {"token": token, "user": current_user}
    send_async_email(current_user.email, subject, template, **context)
    flash(notify_success("A new confirmation email has been sent."))
    return redirect(url_for("auth.unconfirmed"))


@auth_blueprint.route("/unconfirmed")
@login_required
def unconfirmed():
    if current_user.is_email_confirmed:
        return redirect(url_for("dashboard.index"))
    flash(notify_warning("Please confirm your account!"))
    return render_template("auth/unconfirmed.html")


@auth_blueprint.route("/login", methods=["GET", "POST"])
def login():
    context = {}
    login_form = LoginForm()
    context["form"] = login_form
    if login_form.validate_on_submit():
        email = login_form.email.data
        password = login_form.password.data
        user = User.query.filter(
            func.lower(User.email) == func.lower(email)
        ).first()
        if user is None or not user.check_password(password):
            flash(notify_danger("please check your user id and password"))
            return redirect(url_for("auth.login"))
        login_user(user)
        if "next" not in request.form:
            next_url = url_for("dashboard.index")

        else:
            if request.form["next"] == "":
                next_url = url_for("dashboard.index")
            else:
                next_url = get_safe_redirect(request.form["next"])
        return redirect(next_url)
    return render_template("auth/login.html", **context)


@auth_blueprint.route("/logout", methods=["GET"])
@login_required
def logout():
    logout_user()
    flash(notify_success("Successfully logged out"))

    if "next" not in request.args:
        next_url = url_for("dashboard.index")
    else:
        if request.args.get("next") == "":
            next_url = url_for("dashboard.index")
        else:
            next_url = get_safe_redirect(request.args.get("next"))
    return redirect(next_url)
