import uuid
import os
import json

from flask import Blueprint
from flask import jsonify
from flask import redirect
from flask import render_template
from flask import request
from flask import current_app

from flask_login import login_required
from sqlalchemy import exists
from werkzeug.utils import secure_filename
from shopyoapi.file import unique_filename
from shopyoapi.file import delete_file
from shopyoapi.init import db
from shopyoapi.init import ma
from shopyoapi.init import productphotos
from shopyoapi.html import notify_warning

from modules.resource.models import Resource
from modules.product.models import Product

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


class Productchema(ma.Schema):
    class Meta:
        # Fields to expose
        fields = (
            "barcode",
            "name",
            "description",
            "category",
            "price",
            "selling_price",
            "in_stock",
            "discontinued",
        )


product_schema = Productchema()
product_schema = Productchema(many=True)

module_blueprint = globals()["{}_blueprint".format(module_info["module_name"])]

module_name = module_info["module_name"]

@module_blueprint.route("/<category_name>")
@login_required
def list(category_name):
    context = {}
    products = Product.query.filter(Product.category_name == category_name).all()
    context["products"] = products
    context["category"] = category_name

    return render_template("product/list.html", **context)


@module_blueprint.route("/add/<category_name>", methods=["GET", "POST"])
@login_required
def add(category_name):
    context = {}

    has_product = False
    if request.method == "POST":
        barcode = request.form["barcode"]
        name = request.form["name"]
        description = request.form["description"]
        date = request.form["date"]
        price = request.form["price"]
        selling_price = request.form["selling_price"]
        in_stock = request.form["in_stock"]
        if request.form["discontinued"] == "True":
            discontinued = True
        else:
            discontinued = False

        # category = Category.query.filter(
        #     Category.name == category_name).first()
        # print(category, category_name, category.name)
        has_product = db.session.query(
            exists().where(Product.barcode == barcode)
        ).scalar()

        if has_product is False:
            p = Product(
                barcode=barcode,
                name=name,
                in_stock=in_stock,
                category_name=category_name,
                discontinued=discontinued,
            )
            if description:
                p.description = description.strip()
            if date:
                p.date = date.strip()
            if price:
                p.price = price.strip()
            elif not price.strip():
                p.price = 0
            if selling_price:
                p.selling_price = selling_price.strip()

            # if 'photos[]' not in request.files:
            #     flash(notify_warning('no file part'))

            if "photos[]" in request.form:
                files = request.files.getlist("photos[]")
                for file in files:
                    filename = unique_filename(secure_filename(file.filename))
                    file.filename = filename
                    productphotos.save(file)
                    p.resources.append(
                        Resource(
                            type="image", filename=filename, category="product_image"
                        )
                    )

            db.session.add(p)
            db.session.commit()
        context["category"] = category_name
        context["has_product"] = str(has_product)
        context["barcodestr"] = uuid.uuid1()
        return render_template("product/add.html", **context)

    context["category"] = category_name
    context["has_product"] = str(has_product)
    context["barcodestr"] = uuid.uuid1()
    return render_template("product/add.html", **context)


@module_blueprint.route("/delete/<category_name>/<barcode>", methods=["GET", "POST"])
@login_required
def delete(category_name, barcode):
    product = Product.query.filter(
        Product.barcode == barcode and Product.category == category_name
    ).first()
    for resource in product.resources:
        filename = resource.filename
        delete_file(
            os.path.join(current_app.config["UPLOADED_PRODUCTPHOTOS_DEST"], filename)
        )
    product.delete()
    db.session.commit()
    return redirect(url_for('product.list', category_name=category_name))


@module_blueprint.route("/edit/<category_name>/<barcode>", methods=["GET", "POST"])
@login_required
def edit(category_name, barcode):
    context = {}

    product = Product.query.filter(
        Product.barcode == barcode and Product.category == category_name
    ).first()

    context["product"] = product
    context["category"] = category_name
    return render_template("product/edit.html", **context)


@module_blueprint.route("/update", methods=["GET", "POST"])
@login_required
def update():
    # this block is only entered when the form is submitted
    if request.method == "POST":
        barcode = request.form["barcode"]
        old_barcode = request.form["old_barcode"]
        category = request.form["category"]

        name = request.form["name"]
        description = request.form["description"]

        date = request.form["date"]
        price = request.form["price"]
        if not price.strip():
            price = 0
        selling_price = request.form["selling_price"]
        in_stock = request.form["in_stock"]
        if request.form["discontinued"] == "True":
            discontinued = True
        else:
            discontinued = False

        p = Product.query.filter(
            Product.barcode == old_barcode and Product.category == category
        ).first()
        p.barcode = barcode
        p.name = name
        p.description = description
        p.category = category
        p.date = date
        p.price = price
        p.selling_price = selling_price
        p.in_stock = in_stock
        p.discontinued = discontinued
        p.category = category

        if "photos[]" in request.form:
            files = request.files.getlist("photos[]")
            for file in files:
                filename = unique_filename(secure_filename(file.filename))
                file.filename = filename
                productphotos.save(file)
                p.resources.append(
                    Resource(type="image", filename=filename, category="product_image")
                )

        db.session.commit()
        return redirect("/product/list_product/{}".format(category))


@module_blueprint.route("/lookup/<category_name>")
@login_required
def lookup(category_name):
    context = {}

    context["category"] = category_name
    context["fields"] = [
        key.replace("_", " ")
        for key in Product.__table__.columns.keys()
        if key not in ["category_name"]
    ]

    return render_template("product/lookup.html", **context)


# api
@module_blueprint.route(
    "/search/<category_name>/barcode/<user_input>", methods=["GET"]
)
@login_required
def search(category_name, user_input):
    if request.method == "GET":
        print(request.args["field"], request.args["global_search"])
        field = request.args["field"]
        global_search = request.args["global_search"]
        if global_search == "True":
            all_p = Product.query.filter(
                (getattr(Product, field).like("%" + user_input + "%"))
                & (Product.category_name == category_name)
            ).all()
            result = product_schema.dump(all_p)
        else:
            all_p = Product.query.filter(
                getattr(Product, field).like("%" + user_input + "%")
            ).all()
            result = product_schema.dump(all_p)
    return jsonify(result)

# api
@module_blueprint.route("/check/<barcode>", methods=["GET"])
@login_required
def check(barcode):
    has_product = db.session.query(exists().where(Product.barcode == barcode)).scalar()
    return jsonify({"exists": has_product})
