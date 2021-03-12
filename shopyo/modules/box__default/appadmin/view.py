"""
.. module:: AdminViews
   :synopsis: All endpoints of the admin views are defined here.

"""
import json
import os

from flask import Blueprint
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for
from flask import flash

from flask_login import login_required
from sqlalchemy import exists

# from config import Config

from init import db

from .admin import admin_required
from modules.box__default.auth.models import Role
from modules.box__default.auth.models import User
from shopyo.api.html import notify_warning
from shopyo.api.html import notify_success

dirpath = os.path.dirname(os.path.abspath(__file__))
module_info = {}

with open(dirpath + "/info.json") as f:
    module_info = json.load(f)

appadmin_blueprint = Blueprint(
    "appadmin",
    __name__,
    template_folder="templates",
    url_prefix=module_info["url_prefix"],
)


@appadmin_blueprint.route("/")
@login_required
@admin_required
def user_list():
    """
    **Get The List of User**

     Lists all users in the database.

    """
    context = {}
    context["users"] = User.query.all()
    return render_template("appadmin/index.html", **context)


@appadmin_blueprint.route("/add", methods=["GET", "POST"])
@login_required
@admin_required
def user_add():
    """
       **Adds a User**

    adds a user to database.

    """
    context = {}
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        first_name = request.form["first_name"]
        last_name = request.form["last_name"]
        admin_user = request.form.get("is_admin")
        if admin_user == "True":
            is_admin = True
        else:
            is_admin = False

        has_user = db.session.query(
            exists().where(User.email == email)
        ).scalar()

        if not has_user:
            new_user = User()
            new_user.email = email
            new_user.is_admin = is_admin
            new_user.first_name = first_name
            new_user.last_name = last_name
            new_user.password = password

            for key in request.form:
                if key.startswith("role_"):
                    role_id = key.split("_")[1]
                    role = Role.get_by_id(role_id)
                    new_user.roles.append(role)
            new_user.save()
            return redirect(url_for("appadmin.user_add"))

        flash(notify_warning("User with same email already exists"))

    context["roles"] = Role.query.all()
    return render_template("appadmin/add.html", **context)


@appadmin_blueprint.route("/delete/<id>", methods=["GET"])
@login_required
@admin_required
def admin_delete(id):
    """
               **Delete a User**

    :param id: id of the user
    :type id: int

    """
    user = User.query.get(id)

    if user is None:
        flash(notify_warning("Unable to delete. Invalid user id"))
        return redirect("/appadmin")

    user.delete()
    flash(notify_success("User successfully deleted"))
    return redirect("/appadmin")


@appadmin_blueprint.route("/edit/<id>", methods=["GET"])
@login_required
@admin_required
def admin_edit(id):
    """
               **Update information for a User**

    :param id: id of the user
    :type id: int

    """
    context = {}
    user = User.query.get(id)

    if user is None:
        flash(notify_warning("Unable to edit. Invalid user id"))
        return redirect("/appadmin")

    context["user"] = user
    context["user_roles"] = [r.name for r in user.roles]
    context["roles"] = Role.query.all()
    return render_template("appadmin/edit.html", **context)


@appadmin_blueprint.route("/update", methods=["POST"])
@login_required
@admin_required
def admin_update():
    """
    **Update a User record**

    """
    id = request.form["id"]
    password = request.form["password"]
    email = request.form["email"]
    first_name = request.form["first_name"]
    last_name = request.form["last_name"]
    is_admin = request.form.get("is_admin")

    if is_admin:
        is_admin = True
    else:
        is_admin = False

    user = User.query.get(id)

    if user is None:
        flash(notify_warning("Unable to update. User does not exist."))
        return redirect("/admin")

    user.is_admin = is_admin
    user.email = email
    user.first_name = first_name
    user.last_name = last_name
    user.roles[:] = []

    if password.strip():
        user.password = password

    for key in request.form:
        if key.startswith("role_"):
            role_id = key.split("_")[1]
            role = Role.get_by_id(role_id)
            user.roles.append(role)

    user.update()
    flash(notify_success("User successfully updated"))
    return redirect("/appadmin")


@appadmin_blueprint.route("/roles")
@login_required
@admin_required
def roles():
    context = {}
    context["roles"] = Role.query.all()
    return render_template("appadmin/roles.html", **context)


@appadmin_blueprint.route("/roles/add", methods=["POST"])
@login_required
@admin_required
def roles_add():
    if request.method == "POST":
        if not Role.query.filter(Role.name == request.form["name"]).first():
            role = Role(name=request.form["name"])
            role.save()
            flash(notify_success("Role successfully added"))
            return redirect(url_for("appadmin.roles"))
        flash(notify_warning("Role already exists"))
        return redirect(url_for("appadmin.roles"))


@appadmin_blueprint.route("/roles/<role_id>/delete", methods=["GET"])
@login_required
@admin_required
def roles_delete(role_id):
    role = Role.get_by_id(role_id)

    if role is None:
        flash(notify_warning("Unable to delete. Invalid role id"))
        return redirect(url_for("appadmin.roles"))

    role.delete()
    flash(notify_success("Role successfully deleted"))
    return redirect(url_for("appadmin.roles"))


@appadmin_blueprint.route("/roles/update", methods=["POST"])
@login_required
@admin_required
def roles_update():
    if request.method == "POST":
        role = Role.get_by_id(request.form["role_id"])

        if role is None:
            flash(notify_warning("Unable to update. Role does not exist"))
            return redirect(url_for("appadmin.roles"))

        role.name = request.form["role_name"]
        role.update()
        flash(notify_success("Role successfully updated"))

    return redirect(url_for("appadmin.roles"))
