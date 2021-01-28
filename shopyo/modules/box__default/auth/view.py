import json
import os

from flask import Blueprint
from flask import flash
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for

from flask_login import login_required
from flask_login import login_user
from flask_login import logout_user

from shopyoapi.html import notify_danger
from shopyoapi.html import notify_success

from modules.box__default.admin.models import User
from modules.box__default.auth.forms import LoginForm

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


@auth_blueprint.route("/login", methods=["GET", "POST"])
def login():
    context = {}
    login_form = LoginForm()
    context["form"] = login_form
    if login_form.validate_on_submit():
        email = login_form.email.data
        password = login_form.password.data
        user = User.query.filter_by(email=email).first()
        if user is None or not user.check_hash(password):
            flash(notify_danger("please check your user id and password"))
            return redirect(url_for("auth.login"))
        login_user(user)
        return redirect(url_for("dashboard.index"))
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
    flash(notify_success("Successfully logged out"))
    return redirect(url_for("auth.login"))
