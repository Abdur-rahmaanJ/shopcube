"""
.. module:: AdminViews
   :synopsis: All endpoints of the admin views are defined here.

"""
import os
import json
from config import Config
from flask import Blueprint, render_template, request, redirect
from flask import url_for

from flask_login import login_required
from shopyoapi.init import db

from shopyoapi.enhance import base_context
from sqlalchemy import exists

from modules.admin.admin import admin_required
from modules.admin.models import User
from modules.admin.models import Role

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
            
            for key in request.form:
                if key.startswith('role_'):
                    roleid = key.split('_')[1]
                    role = Role.query.get(roleid)
                    new_user.roles.append(role)
            new_user.insert()
            return redirect(url_for('admin.user_add'))

    context['roles'] = Role.query.all()
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
    user = User.query.get(id)
    context['user'] = user
    context['user_roles'] = [r.name for r in user.roles]
    context['roles'] = Role.query.all()
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
    username = request.form["username"]
    admin_user = request.form.get("admin_user")
    if admin_user == "True":
        admin_user = True
    else:
        admin_user = False
    user = User.query.get(id)
    user.set_hash(password)
    user.admin_user = admin_user
    user.username = username
    if password.strip():
        user.set_hash(password)
    user.roles[:] = []
    for key in request.form:
        if key.startswith('role_'):
            roleid = key.split('_')[1]
            role = Role.query.get(roleid) 
            user.roles.append(role)

    user.update()
    return redirect("/admin")

@admin_blueprint.route("/roles")
@login_required
@admin_required
def roles():
    context = base_context()
    context['roles'] = Role.query.all()
    return render_template('admin/roles.html', **context)

@admin_blueprint.route("/roles/add", methods=['POST'])
@login_required
@admin_required
def roles_add():
    if request.method == 'POST':
        if not Role.query.filter(
                  Role.name == request.form['name']
              ).first():
            role = Role(name=request.form['name'])
            role.insert()
    return redirect(url_for('admin.roles'))


@admin_blueprint.route("/roles/<role_id>/delete", methods=['GET'])
@login_required
@admin_required
def roles_delete(role_id):
    role = Role.query.get(role_id)
    role.delete()
    return redirect(url_for('admin.roles'))


@admin_blueprint.route("/roles/update", methods=['POST'])
@login_required
@admin_required
def roles_update():
    if request.method == 'POST':
        role = Role.query.get(request.form['role_id'])
        role.name = request.form['role_name']
        role.update()
    return redirect(url_for('admin.roles'))