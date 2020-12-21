import json
import os

from flask import Blueprint
from flask import current_app
from flask import flash
from flask import jsonify
from flask import redirect
from flask import render_template
from flask import request
from flask import send_from_directory
from flask import url_for

import flask_uploads
from flask_login import login_required
from flask_sqlalchemy import sqlalchemy

from shopyoapi.enhance import get_setting
from shopyoapi.file import delete_file
from shopyoapi.file import unique_sec_filename
from shopyoapi.html import notify_success
from shopyoapi.html import notify_warning
from shopyoapi.init import categoryphotos
from shopyoapi.init import subcategoryphotos
from shopyoapi.validators import is_empty_str

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


@module_blueprint.route(module_info["dashboard"])
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
        if is_empty_str(name):
            return redirect(url_for("category.dashboard"))
        if name.strip() == "uncategorised":
            flash(notify_warning("Category cannot be named as uncategorised"))
            return redirect(url_for("category.dashboard"))
        has_category = Category.category_exists(name)
        if has_category is False:
            category = Category(name=name)
            try:
                if "photo" in request.files:
                    file = request.files["photo"]

                    filename = unique_sec_filename(file.filename)
                    file.filename = filename
                    categoryphotos.save(file)
                    category.resources.append(
                        Resource(
                            type="image",
                            filename=filename,
                            category="category_image",
                        )
                    )
            except flask_uploads.UploadNotAllowed as e:
                pass
            category.insert()
        return render_template("category/add.html", **context)

    context["has_category"] = str(has_category)
    return render_template("category/add.html", **context)


@module_blueprint.route("<name>/delete", methods=["GET", "POST"])
@login_required
def delete(name):

    if name != "uncategorised":

        category = Category.query.filter(Category.name == name).first()

        if len(category.subcategories) != 0:
            flash(
                notify_warning(
                    "please delete all subcategories for category".format(name)
                )
            )
            return url_for("category.dashboard")

        category.delete()
        return redirect(url_for("category.dashboard"))
    else:
        flash(notify_warning("Cannot delete category uncategorised"))
        return redirect(url_for("category.dashboard"))


@module_blueprint.route("/<category_name>/img/<filename>/delete", methods=["GET"])
@login_required
def category_image_delete(category_name, filename):
    resource = Resource.query.filter(Resource.filename == filename).first()
    category = Category.query.filter(Category.name == category_name).first()
    category.resources.remove(resource)
    category.update()
    delete_file(
        os.path.join(current_app.config["UPLOADED_CATEGORYPHOTOS_DEST"], filename)
    )

    return redirect(url_for("category.dashboard"))


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
            category = Category.query.filter_by(name=old_name).first()

            try:
                if "photo" in request.files:
                    file = request.files["photo"]

                    filename = unique_sec_filename(file.filename)
                    file.filename = filename
                    categoryphotos.save(file)
                    category.resources.append(
                        Resource(
                            type="image",
                            filename=filename,
                            category="category_image",
                        )
                    )
            except flask_uploads.UploadNotAllowed as e:
                pass

            category.name = name
            category.update()
        except sqlalchemy.exc.IntegrityError:
            context["message"] = "you cannot modify to an already existing category"
            context["redirect_url"] = "/category/"
            render_template("category/message.html", **context)
        return redirect(url_for("category.dashboard"))


@module_blueprint.route(
    "{}/edit/<category_name>".format(module_info["dashboard"]),
    methods=["GET", "POST"],
)
@login_required
def edit_dashboard(category_name):
    context = {}
    category = Category.query.filter(Category.name == category_name).first()

    context.update({"len": len, "category": category})
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


@module_blueprint.route(
    "{}/<category_name>/sub/".format(module_info["dashboard"]),
    methods=["GET", "POST"],
)
@login_required
def manage_sub(category_name):
    context = {}
    category = Category.query.filter(Category.name == category_name).first()

    context.update({"category": category})
    return render_template("category/manage_sub.html", **context)


@module_blueprint.route(
    "{}/<category_name>/sub/add".format(module_info["dashboard"]),
    methods=["GET", "POST"],
)
@login_required
def add_sub(category_name):
    if request.method == "POST":
        name = request.form["name"]

        if is_empty_str(name):
            flash(notify_warning("Name cannot be empty"))
            return redirect(
                url_for(
                    "category.manage_sub",
                    category_name=subcategory.category.name,
                )
            )

        existing = SubCategory.query.filter(
            (SubCategory.name == name) & (Category.name == category_name)
        ).first()
        if existing:
            flash(notify_warning("Name already exists for category"))
            return redirect(
                url_for(
                    "category.manage_sub",
                    category_name=subcategory.category.name,
                )
            )

        category = Category.query.filter(Category.name == category_name).first()
        subcategory = SubCategory(name=name)

        try:
            if "photo" in request.files:
                file = request.files["photo"]

                filename = unique_sec_filename(file.filename)
                file.filename = filename
                subcategoryphotos.save(file)
                subcategory.resources.append(
                    Resource(
                        type="image",
                        filename=filename,
                        category="subcategory_image",
                    )
                )
        except flask_uploads.UploadNotAllowed as e:
            pass

        category.subcategories.append(subcategory)

        category.update()
        return redirect(url_for("category.manage_sub", category_name=category_name))


@module_blueprint.route(
    "{}/sub/<subcategory_id>/img/edit".format(module_info["dashboard"]),
    methods=["GET", "POST"],
)
@login_required
def edit_sub_img_dashboard(subcategory_id):
    context = {}
    subcategory = SubCategory.query.get(subcategory_id)
    context.update({"len": len, "subcategory": subcategory})
    return render_template("category/edit_img_sub.html", **context)


@module_blueprint.route("/sub/<subcategory_id>/name/edit", methods=["GET", "POST"])
@login_required
def edit_sub_name(subcategory_id):
    if request.method == "POST":
        subcategory = SubCategory.query.get(subcategory_id)
        name = request.form["name"]
        if is_empty_str(name):
            flash(notify_warning("Name cannot be empty"))
            return redirect(
                url_for(
                    "category.manage_sub",
                    category_name=subcategory.category.name,
                )
            )
        category_name = subcategory.category.name
        existing = SubCategory.query.filter(
            (SubCategory.name == name) & (Category.name == category_name)
        ).first()
        if existing:
            flash(notify_warning("Name already exists for category"))
            return redirect(
                url_for(
                    "category.manage_sub",
                    category_name=subcategory.category.name,
                )
            )
        subcategory.name = name
        subcategory.update()
        flash(notify_success("Subcategory name updated successfully!"))
        return redirect(
            url_for("category.manage_sub", category_name=subcategory.category.name)
        )


@module_blueprint.route("/sub/<subcategory_id>/img/edit", methods=["GET", "POST"])
@login_required
def edit_sub_img(subcategory_id):
    if request.method == "POST":
        subcategory = SubCategory.query.get(subcategory_id)
        try:
            if "photo" in request.files:
                file = request.files["photo"]

                filename = unique_sec_filename(file.filename)
                file.filename = filename
                subcategoryphotos.save(file)
                subcategory.resources.append(
                    Resource(
                        type="image",
                        filename=filename,
                        category="subcategory_image",
                    )
                )
        except flask_uploads.UploadNotAllowed as e:
            pass
        subcategory.update()
        return redirect(
            url_for(
                "category.edit_sub_img_dashboard",
                subcategory_id=subcategory.id,
            )
        )


@module_blueprint.route("/sub/<subcategory_id>/img/<filename>/delete", methods=["GET"])
@login_required
def subcategory_image_delete(subcategory_id, filename):
    resource = Resource.query.filter(Resource.filename == filename).first()
    subcategory = SubCategory.query.get(subcategory_id)
    subcategory.resources.remove(resource)
    subcategory.update()
    delete_file(
        os.path.join(current_app.config["UPLOADED_SUBCATEGORYPHOTOS_DEST"], filename)
    )

    return redirect(
        url_for("category.edit_sub_img_dashboard", subcategory_id=subcategory_id)
    )


@module_blueprint.route("/sub/<subcategory_id>/delete", methods=["GET", "POST"])
@login_required
def sub_delete(subcategory_id):
    subcategory = SubCategory.query.get(subcategory_id)
    category_name = subcategory.name
    if (
        subcategory.name == "uncategorised"
        and subcategory.category.name == "uncategorised"
    ):
        flash(
            notify_warning(
                "Cannot delete subcategory uncategorised of catgeory uncategorised"
            )
        )
        return redirect(url_for("category.manage_sub", category_name=category_name))

    uncategorised_sub = SubCategory.query.filter(
        (SubCategory.name == "uncategorised")
        & (SubCategory.category_name == "uncategorised")
    ).first()

    for product in subcategory.products:
        uncategorised_sub.products.append(product)
    uncategorised_sub.update()
    subcategory.products = []
    category = subcategory.category
    category.subcategories.remove(subcategory)
    category.update()

    # for resource in subcategory.resources:
    #     filename = resource.filename
    #     resource.delete()
    #     delete_file(
    #         os.path.join(current_app.config["UPLOADED_SUBCATEGORYPHOTOS_DEST"], filename)
    #     )
    # subcategory.delete()

    ## add for products change
    return redirect(url_for("category.manage_sub", category_name=category_name))


@module_blueprint.route(
    "<category_id>/{}/sub".format(module_info["dashboard"]),
    methods=["GET", "POST"],
)
@login_required
def choose_sub_dashboard(category_id):
    context = {}
    category = Category.query.get(category_id)

    context.update({"category": category})
    return render_template("category/choose_sub.html", **context)


#
# serve files
#


@module_blueprint.route("/sub/file/<filename>", methods=["GET"])
def subcategory_image(filename):
    if filename == "default":
        return send_from_directory(
            os.path.join(current_app.config["BASE_DIR"], "static", "default"),
            "default_subcategory.jpg",
        )
    return send_from_directory(
        current_app.config["UPLOADED_SUBCATEGORYPHOTOS_DEST"], filename
    )


@module_blueprint.route("/file/<filename>", methods=["GET"])
def category_image(filename):

    return send_from_directory(
        current_app.config["UPLOADED_CATEGORYPHOTOS_DEST"], filename
    )
