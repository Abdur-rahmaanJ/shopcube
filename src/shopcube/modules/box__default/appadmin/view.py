"""
.. module:: AdminViews
   :synopsis: All endpoints of the admin views are defined here.

"""
from flask import flash
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for
from flask_login import login_required
from init import db
from modules.box__default.auth.models import Role
from modules.box__default.auth.models import User
from shopyo.api.html import notify_success
from shopyo.api.html import notify_warning
from shopyo.api.module import ModuleHelp
from sqlalchemy import exists

from .admin import admin_required

# from config import Config

mhelp = ModuleHelp(__file__, __name__)
globals()[mhelp.blueprint_str] = mhelp.blueprint
module_blueprint = globals()[mhelp.blueprint_str]


@module_blueprint.route("/")
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


@module_blueprint.route("/add", methods=["GET", "POST"])
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

        has_user = db.session.query(exists().where(User.email == email)).scalar()

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

        flash("User with same email already exists", "warning")

    context["roles"] = Role.query.all()
    return render_template("appadmin/add.html", **context)


@module_blueprint.route("/delete/<id>", methods=["GET"])
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
        flash("Unable to delete. Invalid user id", "error")
        return redirect("/appadmin")

    user.delete()
    flash("User successfully deleted", "ok")
    return redirect("/appadmin")


@module_blueprint.route("/edit/<id>", methods=["GET"])
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
        flash("Unable to edit. Invalid user id", "error")
        return redirect("/appadmin")

    context["user"] = user
    context["user_roles"] = [r.name for r in user.roles]
    context["roles"] = Role.query.all()
    return render_template("appadmin/edit.html", **context)


@module_blueprint.route("/update", methods=["POST"])
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
        flash("Unable to update. User does not exist.", "error")
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
    flash("User successfully updated", "ok")
    return redirect("/appadmin")


@module_blueprint.route("/roles")
@login_required
@admin_required
def roles():
    context = {}
    context["roles"] = Role.query.all()
    return render_template("appadmin/roles.html", **context)


@module_blueprint.route("/roles/add", methods=["POST"])
@login_required
@admin_required
def roles_add():
    if request.method == "POST":
        if not Role.query.filter(Role.name == request.form["name"]).first():
            role = Role(name=request.form["name"])
            role.save()
            flash("Role successfully added", "ok")
            return redirect(url_for("appadmin.roles"))
        flash("Role already exists", "warning")
        return redirect(url_for("appadmin.roles"))


@module_blueprint.route("/roles/<role_id>/delete", methods=["GET"])
@login_required
@admin_required
def roles_delete(role_id):
    role = Role.get_by_id(role_id)

    if role is None:
        flash("Unable to delete. Invalid role id", "warning")
        return redirect(url_for("appadmin.roles"))

    role.delete()
    flash("Role successfully deleted", "ok")
    return redirect(url_for("appadmin.roles"))


@module_blueprint.route("/roles/update", methods=["POST"])
@login_required
@admin_required
def roles_update():
    if request.method == "POST":
        role = Role.get_by_id(request.form["role_id"])

        if role is None:
            flash("Unable to update. Role does not exist", "warning")
            return redirect(url_for("appadmin.roles"))

        role.name = request.form["role_name"]
        role.update()
        flash("Role successfully updated", "ok")

    return redirect(url_for("appadmin.roles"))
