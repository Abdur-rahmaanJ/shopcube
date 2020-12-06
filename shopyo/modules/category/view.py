import json
import os

from flask import Blueprint
from flask import jsonify
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for
from flask import send_from_directory
from flask import current_app
from werkzeug.utils import secure_filename

from flask_login import login_required
from flask_sqlalchemy import sqlalchemy

from shopyoapi.enhance import get_setting
from shopyoapi.file import unique_filename
from shopyoapi.init import subcategoryphotos

from modules.category.models import Category
from modules.category.models import SubCategory
from modules.resource.models import Resource

dirpath = os.path.dirname(os.path.abspath(__file__))
module_info = {}

with open(dirpath + "/info.json") as f:
    module_info = json.load(f)

globals()["{}_blueprint".format(module_info["module_name"])] = Blueprint(
    "{}".format(module_info["module_name"]),
    __name__,
    template_folder="templates",
    url_prefix=module_info["url_prefix"],
)

module_blueprint = globals()["{}_blueprint".format(module_info["module_name"])]

module_name = module_info["module_name"]


@module_blueprint.route(module_info["panel_redirect"])
@login_required
def dashboard():
    context = {}
    context["categorys"] = Category.query.all()
    context["active_page"] = get_setting("SECTION_NAME")
    return render_template("category/dashboard.html", **context)


@module_blueprint.route("/add", methods=["GET", "POST"])
@login_required
def add():
    context = {}

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


@module_blueprint.route("/delete/<name>", methods=["GET", "POST"])
@login_required
def delete(name):
    category = Category.query.filter(Category.name == name).first()
    category.delete()
    return redirect("/category")


@module_blueprint.route("/update", methods=["GET", "POST"])
@login_required
def update():
    context = {}

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
            context["message"] = "you cannot modify to an already existing category"
            context["redirect_url"] = "/category/"
            render_template("category/message.html", **context)
        return redirect("/category/")


@module_blueprint.route("{}/edit/<category_name>".format(module_info["panel_redirect"]), methods=["GET", "POST"])
@login_required
def edit(category_name):
    context = {}
    context["category_name"] = category_name
    return render_template("category/edit.html", **context)

# api
@module_blueprint.route("/check/<category_name>", methods=["GET"])
@login_required
def check(category_name):
    has_category = Category.category_exists(category_name)
    return jsonify({"exists": has_category})

#
# subcategory
#

@module_blueprint.route("{}/<category_name>/sub/".format(module_info["panel_redirect"]), methods=["GET", "POST"])
@login_required
def manage_sub(category_name):
    context = {}
    category = Category.query.filter(Category.name == category_name).first()

    context.update({
        'category': category
        })
    return render_template("category/manage_sub.html", **context)

@module_blueprint.route("{}/<category_name>/sub/add".format(module_info["panel_redirect"]), methods=["GET", "POST"])
@login_required
def add_sub(category_name):
    if request.method == 'POST':
        name = request.form['name']

        if name.strip() == '':
            flash(notify_warning('subcategory name cannot be empty!'))
            return redirect(url_for('add_sub', category_name=category_name))

        category = Category.query.filter(Category.name == category_name).first()
        subcategory = SubCategory(name=name)
        

        if "photo" in request.files:
            file = request.files['photo']
            
            filename = unique_filename(secure_filename(file.filename))
            file.filename = filename
            subcategoryphotos.save(file)
            subcategory.resources.append(
                Resource(
                    type="image", filename=filename, category="subcategory_image"
                )
            )

        category.subcategories.append(subcategory)

        category.update()
        return redirect(url_for('category.manage_sub', category_name=category_name))


#
# serve files
#

@module_blueprint.route("/sub/file/<filename>", methods=["GET"])
def subcategory_image(filename):

    return send_from_directory(
        current_app.config["UPLOADED_SUBCATEGORYPHOTOS_DEST"], filename
    )

@module_blueprint.route("{}/sub/<subcategory_name>/img/edit".format(module_info["panel_redirect"]), methods=["GET", "POST"])
@login_required
def edit_sub_img(subcategory_name):

    return ''