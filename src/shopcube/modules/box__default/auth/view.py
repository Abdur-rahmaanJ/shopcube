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

from shopyo.api.html import notify_danger
from shopyo.api.html import notify_success

from modules.box__default.admin.models import User
from modules.box__default.auth.forms import LoginForm, RegistrationForm

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
    if request.method == 'POST':
        if login_form.validate_on_submit():
            email = login_form.email.data
            password = login_form.password.data
            user = User.query.filter(User.email==email).first()
            print(email, password, user)
            if user is None or not user.check_hash(password):
                flash('')
                flash(notify_danger("please check your user id and password"))
                return redirect(url_for("www.index"))
            login_user(user)
            if user.is_admin:
                flash(notify_success('Successfully logged in!'))
                return redirect(url_for("dashboard.index"))
            elif user.is_customer:
                flash(notify_success('Successfully logged in!'))
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
    flash(notify_success("Successfully logged out"))
    return redirect(url_for('www.index'))
    # return redirect(url_for("auth.login"))
