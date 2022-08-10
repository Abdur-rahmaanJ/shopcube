import json
import os
import uuid

from flask import Blueprint
from flask import current_app

# from flask import flash
from flask import jsonify
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for

import flask_uploads
from flask_login import login_required
from sqlalchemy import exists
from werkzeug.utils import secure_filename

from shopyo.api.file import delete_file
from shopyo.api.file import unique_filename
from init import db
from init import ma
from init import productphotos

from modules.box__ecommerce.category.models import SubCategory
from modules.box__ecommerce.product.models import Product
from modules.box__ecommerce.product.models import Size
from modules.box__ecommerce.product.models import Color
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


class Productchema(ma.Schema):
    class Meta:
        # Fields to expose
        fields = (
            "barcode",
            "name",
            "description",
            "price",
            "selling_price",
            "in_stock",
            "discontinued",
        )


product_schema = Productchema()
product_schema = Productchema(many=True)

module_blueprint = globals()["{}_blueprint".format(module_info["module_name"])]

module_name = module_info["module_name"]


@module_blueprint.route("/sub/<subcategory_id>/dashboard")
@login_required
def list(subcategory_id):
    context = {}
    subcategory = SubCategory.query.get(subcategory_id)

    context.update({"subcategory": subcategory})
    return render_template("product/list.html", **context)


@module_blueprint.route(
    "/sub/<subcategory_id>/add/dashboard", methods=["GET", "POST"]
)
@login_required
def add_dashboard(subcategory_id):
    context = {}

    has_product = False
    subcategory = SubCategory.query.get(subcategory_id)
    context["subcategory"] = subcategory
    context["has_product"] = str(has_product)
    context["barcodestr"] = uuid.uuid1()
    return render_template("product/add.html", **context)


@module_blueprint.route("/sub/<subcategory_id>/add", methods=["GET", "POST"])
@login_required
def add(subcategory_id):

    if request.method == "POST":

        subcategory = SubCategory.query.get(subcategory_id)
        barcode = request.form["barcode"]
        name = request.form["name"]
        description = request.form["description"]
        date = request.form["date"]
        price = request.form["price"]
        selling_price = request.form["selling_price"]
        in_stock = request.form["in_stock"]
        colors = request.form["colors"]
        sizes = request.form["sizes"]

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

            sizes = sizes.strip().strip('\n')
            sizes = [s.strip('\r') for s in sizes.split('\n') if s.strip()]
            sizes = [Size(name=s) for s in sizes]
            p.sizes = sizes

            colors = colors.strip().strip('\n')
            colors = [c.strip('\r') for c in colors.split('\n') if c.strip()]
            colors = [Color(name=c) for c in colors]
            p.colors = colors

            # if 'photos[]' not in request.files:
            #     flash(notify_warning('no file part'))
            try:
                if "photos[]" in request.files:
                    files = request.files.getlist("photos[]")
                    for file in files:
                        filename = unique_filename(
                            secure_filename(file.filename)
                        )
                        file.filename = filename
                        productphotos.save(file)
                        p.resources.append(
                            Resource(
                                type="image",
                                filename=filename,
                                category="product_image",
                            )
                        )
            except flask_uploads.UploadNotAllowed as e:
                pass

            subcategory.products.append(p)
            subcategory.update()
            return redirect(
                url_for("product.add_dashboard", subcategory_id=subcategory_id)
            )


@module_blueprint.route("/<barcode>/delete", methods=["GET", "POST"])
@login_required
def delete(barcode):
    product = Product.query.filter(Product.barcode == barcode).first()
    subcategory = product.subcategory
    for resource in product.resources:
        filename = resource.filename
        delete_file(
            os.path.join(
                current_app.config["UPLOADED_PRODUCTPHOTOS_DEST"], filename
            )
        )
    product.delete()
    db.session.commit()
    return redirect(url_for("product.list", subcategory_id=subcategory.id))


@module_blueprint.route("/<barcode>/edit/dashboard", methods=["GET", "POST"])
@login_required
def edit_dashboard(barcode):
    context = {}

    product = Product.query.filter(Product.barcode == barcode).first()

    context.update(
        {"len": len, "product": product, "subcategory": product.subcategory}
    )
    return render_template("product/edit.html", **context)


@module_blueprint.route(
    "/sub/<subcategory_id>/update", methods=["GET", "POST"]
)
@login_required
def update(subcategory_id):
    # this block is only entered when the form is submitted
    if request.method == "POST":
        subcategory = SubCategory.query.get(subcategory_id)
        barcode = request.form["barcode"]
        old_barcode = request.form["old_barcode"]
        # category = request.form["category"]

        name = request.form["name"]
        description = request.form["description"]

        date = request.form["date"]
        price = request.form["price"]
        product_id = request.form['product_id']
        if not price.strip():
            price = 0
        selling_price = request.form["selling_price"]
        in_stock = request.form["in_stock"]
        colors = request.form["colors"]
        sizes = request.form["sizes"]

        if request.form["discontinued"] == "True":
            discontinued = True
        else:
            discontinued = False

        p = Product.query.get(product_id)
        p.barcode = barcode
        p.name = name
        p.description = description
        p.date = date
        p.price = price
        p.selling_price = selling_price
        p.in_stock = in_stock
        p.discontinued = discontinued

        with db.session.no_autoflush:
            p.sizes.clear()
            sizes = sizes.strip().strip('\n')
            sizes = [s.strip('\r') for s in sizes.split('\n') if s.strip()]
            sizes = [Size(name=s, product_id=p.id) for s in sizes]
            p.sizes.extend(sizes)
        with db.session.no_autoflush:
            p.colors.clear()
            colors = colors.strip().strip('\n')
            colors = [c.strip('\r') for c in colors.split('\n') if c.strip()]
            colors = [Color(name=c, product_id=p.id) for c in colors]
            p.colors.extend(colors)
        # p.category = category
        try:
            if "photos[]" in request.files:

                files = request.files.getlist("photos[]")
                for file in files:
                    filename = unique_filename(secure_filename(file.filename))
                    file.filename = filename
                    productphotos.save(file)
                    p.resources.append(
                        Resource(
                            type="image",
                            filename=filename,
                            category="product_image",
                        )
                    )
        except flask_uploads.UploadNotAllowed as e:
            pass
        db.session.commit()
        return redirect(url_for("product.list", subcategory_id=subcategory.id))


@module_blueprint.route("sub/<subcategory_id>/lookup")
@login_required
def lookup(subcategory_id):
    context = {}

    subcategory = SubCategory.query.get(subcategory_id)
    context["subcategory"] = subcategory
    context["fields"] = [
        key.replace("_", " ")
        for key in Product.__table__.columns.keys()
        if key not in ["category_name"]
    ]

    return render_template("product/lookup.html", **context)


# api
@module_blueprint.route(
    "sub/<subcategory_id>/search/<user_input>", methods=["GET"]
)
@login_required
def search(subcategory_id, user_input):
    if request.method == "GET":
        subcategory = SubCategory.query.get(subcategory_id)
        print(request.args["field"], request.args["global_search"])
        field = request.args["field"]
        global_search = request.args["global_search"]
        if global_search == "True":
            subcategory_name = subcategory.name
            all_p = Product.query.filter(
                (getattr(Product, field).like("%" + user_input + "%"))
                & (Product.subcategory_name == subcategory_name)
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
    has_product = db.session.query(
        exists().where(Product.barcode == barcode)
    ).scalar()
    return jsonify({"exists": has_product})


#
# files
#


@module_blueprint.route(
    "/<filename>/product/<barcode>/delete", methods=["GET"]
)
def image_delete(filename, barcode):
    resource = Resource.query.filter(Resource.filename == filename).first()
    product = Product.query.filter(Product.barcode == barcode).first()
    product.resources.remove(resource)
    product.update()
    delete_file(
        os.path.join(
            current_app.config["UPLOADED_PRODUCTPHOTOS_DEST"], filename
        )
    )

    return redirect(url_for("product.edit_dashboard", barcode=barcode))
