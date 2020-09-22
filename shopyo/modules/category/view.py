import os
import json

from flask import Blueprint
from flask import render_template
from flask import request
from flask import redirect
from flask import jsonify
from flask_sqlalchemy import sqlalchemy
from modules.category.models import Category


from flask_login import login_required

from shopyoapi.enhance import base_context
from shopyoapi.enhance import get_setting


dirpath = os.path.dirname(os.path.abspath(__file__))
module_info = {}

with open(dirpath + "/info.json") as f:
    module_info = json.load(f)

category_blueprint = Blueprint(
    "category",
    __name__,
    template_folder="templates",
    url_prefix=module_info["url_prefix"],
)


@category_blueprint.route("/")
@login_required
def category():
    context = base_context()
    context["categorys"] = Category.query.all()
    context["active_page"] = get_setting("SECTION_NAME")
    return render_template("category/index.html", **context)


@category_blueprint.route("/add", methods=["GET", "POST"])
@login_required
def category_add():
    context = base_context()

    has_category = False
    if request.method == "POST":
        name = request.form["name"]
        has_category = Category.category_exists(name)
        if has_category is False:
            m = Category(name=name)
            m.insert()
        return render_template("category/add.html", **context)

    context["has_category"] = str(has_category)
    return render_template("category/add.html", **context)


@category_blueprint.route("/delete/<name>", methods=["GET", "POST"])
@login_required
def category_delete(name):
    category = Category.query.filter(Category.name == name).first()
    category.delete()
    return redirect("/category")


@category_blueprint.route("/update", methods=["GET", "POST"])
@login_required
def category_update():
    context = base_context()

    if (
        request.method == "POST"
    ):  # this block is only entered when the form is submitted
        name = request.form["category_name"]
        old_name = request.form["old_category_name"]
        try:
            m = Category.query.filter_by(name=old_name).first()
            m.name = name
            m.update()
        except sqlalchemy.exc.IntegrityError:
            context[
                "message"
            ] = "you cannot modify to an already existing category"
            context["redirect_url"] = "/category/"
            render_template("category/message.html", **context)
        return redirect("/category/")


@category_blueprint.route("/edit/<category_name>", methods=["GET", "POST"])
@login_required
def category_edit(category_name):
    context = base_context()
    context["category_name"] = category_name
    return render_template("category/edit.html", **context)


# api
@category_blueprint.route("/check/<category_name>", methods=["GET"])
@login_required
def check(category_name):
    has_category = Category.category_exists(category_name)
    return jsonify({"exists": has_category})
