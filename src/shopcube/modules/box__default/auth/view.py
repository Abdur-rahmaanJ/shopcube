import json
import os

from flask import Blueprint
from flask import current_app
from flask import flash
from flask import redirect
from flask import render_template
from flask import request
from flask import session
from flask import url_for
from flask_login import login_required
from flask_login import login_user
from flask_login import logout_user
from flask_login import user_logged_out
from flask_login.utils import _get_user
from modules.box__default.admin.models import User
from modules.box__default.auth.forms import LoginForm
from modules.box__default.auth.forms import RegistrationForm
from shopyo.api.html import notify_danger
from shopyo.api.html import notify_success

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
    context["form"] = reg_form

    if request.method == "POST":

        if reg_form.validate_on_submit():

            email = reg_form.email.data
            password = reg_form.password.data

            # add the user to the db
            User.create(email=email, password=password)

            flash(notify_success("Registered successfully! Please Log In"))
            return redirect(url_for("auth.login"))

    return render_template("auth/register.html", **context)


@auth_blueprint.route("/login", methods=["GET", "POST"])
def login():
    context = {}
    login_form = LoginForm()
    context["form"] = login_form
    if request.method == "POST":
        if login_form.validate_on_submit():
            email = login_form.email.data
            password = login_form.password.data
            user = User.query.filter(User.email == email).first()
            if user is None or not user.check_hash(password):
                flash("")
                flash(notify_danger("please check your user id and password"))
                return redirect(url_for("www.index"))
            login_user(user)
            if user.is_admin:
                flash(notify_success("Successfully logged in!"))
                return redirect(url_for("dashboard.index"))
            elif user.is_customer:
                flash(notify_success("Successfully logged in!"))
                return redirect(url_for("shop.homepage"))

    return render_template("auth/login.html", **context)


@auth_blueprint.route("/shop", methods=["GET", "POST"])
def shop_login():
    context = {}
    login_form = LoginForm()
    context["form"] = login_form
    if request.method == "POST":
        if login_form.validate_on_submit():
            email = login_form.email.data
            password = login_form.password.data
            user = User.query.filter_by(email=email).first()
            if user is None or not user.check_hash(password):
                flash(notify_danger("please check your user id and password"))
                return redirect(url_for("shop.checkout"))
            login_user(user)
            return redirect(url_for("shop.checkout"))
    return render_template("auth/shop_login.html", **context)


@auth_blueprint.route("/logout")
@login_required
def logout():
    logout_user()
    user = _get_user()

    if "_user_id" in session:
        session.pop("_user_id")

    if "_fresh" in session:
        session.pop("_fresh")

    if "_id" in session:
        session.pop("_id")

    cookie_name = current_app.config.get("REMEMBER_COOKIE_NAME")
    if cookie_name in request.cookies:
        session["_remember"] = "clear"
    if "_remember_seconds" in session:
        session.pop("_remember_seconds")

    user_logged_out.send(current_app._get_current_object(), user=user)

    current_app.login_manager._update_request_context_with_user()

    flash(notify_success("Successfully logged out"))
    return redirect(url_for("www.index"))
    # return redirect(url_for("auth.login"))
