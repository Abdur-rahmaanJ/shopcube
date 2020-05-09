"""
.. module:: AdminViews
   :synopsis: All endpoints of the admin views are defined here.

"""
import os
import json

from flask import Blueprint, render_template, request, redirect

from flask_login import login_required
from shopyoapi.init import db

from shopyoapi.enhance import base_context
from sqlalchemy import exists
from modules.admin.admin import admin_required
from modules.admin.models import User

dirpath = os.path.dirname(os.path.abspath(__file__))
module_info = {}

with open(dirpath + "/info.json") as f:
    module_info = json.load(f)

admin_blueprint = Blueprint(
    "admin",
    __name__,
    template_folder="templates",
    url_prefix=module_info["url_prefix"],
)


@admin_blueprint.route("/")
@login_required
@admin_required
def user_list():
    """
           **Get The List of User**

            Lists all users in the database.

    """
    context = base_context()
    context["users"] = User.query.all()
    return render_template("admin/index.html", **context)


@admin_blueprint.route("/add", methods=["GET", "POST"])
@login_required
@admin_required
def user_add():
    """
               **Adds a User**

            adds a user to database.

    """
    context = base_context()
    if request.method == "POST":
        username = request.form["name"]
        password = request.form["password"]
        admin_user = request.form.get("admin_user")
        if admin_user == "True":
            admin_user = True
        else:
            admin_user = False

        has_user = db.session.query(
            exists().where(User.username == username)).scalar()

        if has_user is False:
            new_user = User()
            new_user.username = username
            new_user.admin_user = admin_user
            new_user.set_hash(password)
            new_user.save()
            return render_template("admin/add.html", **context)
    return render_template("admin/add.html", **context)


@admin_blueprint.route("/delete/<id>", methods=["GET"])
@login_required
@admin_required
def admin_delete(id):
    """
                   **Delete a User**

        :param id: id of the user
        :type id: int

    """
    user = User.query.get(id)
    user.delete()
    return redirect("/admin")


@admin_blueprint.route("/edit/<id>", methods=["GET"])
@login_required
@admin_required
def admin_edit(id):
    """
                   **Update information for a User**

        :param id: id of the user
        :type id: int

    """
    context = base_context()
    u = User.query.get(id)
    context["id"] = u.id
    context["username"] = u.username
    context["password"] = u.password
    context["admin_user"] = u.admin_user
    return render_template("admin/edit.html", **context)


@admin_blueprint.route("/update", methods=["POST"])
@login_required
@admin_required
def admin_update():
    """
                   **Update a User record**

    """
    id = request.form["id"]
    password = request.form["password"]
    admin_user = request.form.get("admin_user")
    if admin_user == "True":
        admin_user = True
    else:
        admin_user = False
    u = User.query.get(id)
    u.set_hash(password)
    u.admin_user = admin_user
    u.save()
    return redirect("/admin")
