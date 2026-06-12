import os
import uuid

from flask import current_app
from flask import flash
from flask import jsonify
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for

import flask_uploads
from flask_login import login_required
from shopyo.api.file import delete_file
from shopyo.api.file import unique_filename
from shopyo.api.html import notify_warning
from shopyo.api.module import ModuleHelp
from shopyo_appadmin.admin import admin_required
from sqlalchemy import exists
from werkzeug.utils import secure_filename

from init import db
from init import productphotos

from modules.box__ecommerce.category.models import SubCategory
from modules.box__ecommerce.product.models import Color
from modules.box__ecommerce.product.models import Product
from modules.box__ecommerce.product.models import Size
from modules.box__ecommerce.product.models import StockAdjustment
from modules.box__ecommerce.product.models import BundleComponent
from modules.box__ecommerce.vendor.models import Vendor
from modules.resource.models import Resource

from marshmallow_sqlalchemy import SQLAlchemySchema, auto_field

mhelp = ModuleHelp(__file__, __name__)
globals()[mhelp.blueprint_str] = mhelp.blueprint

class ProductSchema(SQLAlchemySchema):
    class Meta:
        model = Product
        load_instance = True  # Optional: deserialize to model instances

        barcode = auto_field()
        name = auto_field()
        description = auto_field()
        price = auto_field()
        selling_price = auto_field()
        in_stock = auto_field()
        discontinued = auto_field()



product_schema = ProductSchema()
product_schema = ProductSchema(many=True)

module_blueprint = globals()[mhelp.blueprint_str]


@module_blueprint.route("/sub/<subcategory_id>/dashboard")
@login_required
@admin_required
def list(subcategory_id):
    context = {}
    subcategory = SubCategory.query.get(subcategory_id)

    context.update({"subcategory": subcategory})
    return render_template("product/list.html", **context)


@module_blueprint.route(
    "/sub/<subcategory_id>/add/dashboard", methods=["GET", "POST"]
)
@login_required
@admin_required
def add_dashboard(subcategory_id):
    context = {}

    has_product = False
    subcategory = SubCategory.query.get(subcategory_id)
    context["subcategory"] = subcategory
    context["has_product"] = str(has_product)
    context["barcodestr"] = uuid.uuid1()
    context["vendors"] = Vendor.query.order_by(Vendor.name).all()
    return render_template("product/add.html", **context)


@module_blueprint.route("/sub/<subcategory_id>/add", methods=["GET", "POST"])
@login_required
@admin_required
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
        min_stock = request.form.get("min_stock", 0)
        colors = request.form["colors"]
        sizes = request.form["sizes"]

        if request.form["discontinued"] == "True":
            discontinued = True
        else:
            discontinued = False

        has_product = db.session.query(
            exists().where(Product.barcode == barcode)
        ).scalar()

        if has_product is False:
            p = Product(
                barcode=barcode,
                name=name,
                in_stock=in_stock,
                min_stock=min_stock,
                discontinued=discontinued,
            )
            vendor_id = request.form.get("vendor_id")
            if vendor_id:
                p.vendor_id = int(vendor_id)

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
            cost_price = request.form.get("cost_price")
            if cost_price:
                p.cost_price = cost_price.strip()

            sizes = sizes.strip().strip("\n")
            sizes = [s.strip("\r") for s in sizes.split("\n") if s.strip()]
            sizes = [Size(name=s) for s in sizes]
            p.sizes = sizes

            colors = colors.strip().strip("\n")
            colors = [c.strip("\r") for c in colors.split("\n") if c.strip()]
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
            except flask_uploads.UploadNotAllowed:
                flash(notify_warning("File type not allowed for product photo"))

            subcategory.products.append(p)
            subcategory.update()
            return redirect(
                url_for("product.add_dashboard", subcategory_id=subcategory_id)
            )


@module_blueprint.route("/<barcode>/delete", methods=["POST"])
@login_required
@admin_required
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
@admin_required
def edit_dashboard(barcode):
    context = {}

    product = Product.query.filter(Product.barcode == barcode).first()

    context.update(
        {"len": len, "product": product, "subcategory": product.subcategory}
    )
    context["vendors"] = Vendor.query.order_by(Vendor.name).all()
    return render_template("product/edit.html", **context)


@module_blueprint.route(
    "/sub/<subcategory_id>/update", methods=["GET", "POST"]
)
@login_required
@admin_required
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
        product_id = request.form["product_id"]
        if not price.strip():
            price = 0
        selling_price = request.form["selling_price"]
        in_stock = request.form["in_stock"]
        min_stock = request.form.get("min_stock", 0)
        colors = request.form["colors"]
        sizes = request.form["sizes"]

        if request.form["discontinued"] == "True":
            discontinued = True
        else:
            discontinued = False

        p = Product.query.get(product_id)
        old_stock = p.in_stock
        p.barcode = barcode
        p.name = name
        p.description = description
        p.date = date
        p.price = price
        p.selling_price = selling_price
        p.cost_price = request.form.get("cost_price", 0)
        p.in_stock = in_stock
        p.min_stock = min_stock
        p.discontinued = discontinued
        vendor_id = request.form.get("vendor_id")
        p.vendor_id = int(vendor_id) if vendor_id else None

        stock_diff = int(in_stock) - old_stock
        if stock_diff != 0:
            p.log_adjustment(
                stock_diff,
                "manual edit",
                f"Stock changed from {old_stock} to {in_stock} via product edit"
            )

        with db.session.no_autoflush:
            p.sizes.clear()
            sizes = sizes.strip().strip("\n")
            sizes = [s.strip("\r") for s in sizes.split("\n") if s.strip()]
            sizes = [Size(name=s, product_id=p.id) for s in sizes]
            p.sizes.extend(sizes)
        with db.session.no_autoflush:
            p.colors.clear()
            colors = colors.strip().strip("\n")
            colors = [c.strip("\r") for c in colors.split("\n") if c.strip()]
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
        except flask_uploads.UploadNotAllowed:
            flash(notify_warning("File type not allowed for product photo"))
        db.session.commit()
        return redirect(url_for("product.list", subcategory_id=subcategory.id))


@module_blueprint.route("sub/<subcategory_id>/lookup")
@login_required
@admin_required
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


# Allowlist of searchable Product column names — prevents attribute injection
# via getattr() with user-controlled field names
_SEARCHABLE_FIELDS = {
    "barcode", "name", "description", "date", "price",
    "selling_price", "in_stock", "min_stock", "cost_price",
    "discontinued", "is_onsale", "is_featured",
}


# api
@module_blueprint.route(
    "sub/<subcategory_id>/search/<user_input>", methods=["GET"]
)
@login_required
@admin_required
def search(subcategory_id, user_input):
    if request.method == "GET":
        subcategory = SubCategory.query.get(subcategory_id)
        field = request.args.get("field", "")
        global_search = request.args.get("global_search", "False")

        # Normalize display names (e.g. "selling price") to column names
        field = field.replace(" ", "_")

        # Validate against allowlist before passing to getattr()
        if field not in _SEARCHABLE_FIELDS:
            return jsonify({"error": f"Invalid search field: {field}"}), 400

        column_attr = getattr(Product, field)

        if global_search == "True":
            all_p = Product.query.filter(
                (column_attr.like(f"%{user_input}%"))
                & (Product.subcategory == subcategory)
            ).all()
        else:
            all_p = Product.query.filter(
                column_attr.like(f"%{user_input}%")
            ).all()
        result = product_schema.dump(all_p)
    return jsonify(result)


# api
@module_blueprint.route("/check/<barcode>", methods=["GET"])
@login_required
@admin_required
def check(barcode):
    has_product = db.session.query(
        exists().where(Product.barcode == barcode)
    ).scalar()
    return jsonify({"exists": has_product})


#
# files
#


@module_blueprint.route(
    "/<filename>/product/<barcode>/delete", methods=["POST"]
)
@login_required
@admin_required
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


@module_blueprint.route("/<barcode>/adjustments", methods=["GET"])
@login_required
@admin_required
def adjustments(barcode):
    product = Product.query.filter(Product.barcode == barcode).first_or_404()
    context = {"product": product}
    context["adjustments"] = StockAdjustment.query.filter_by(product_id=product.id)\
        .order_by(StockAdjustment.created_at.desc()).all()
    return render_template("product/adjustments.html", **context)


@module_blueprint.route("/<barcode>/adjust", methods=["POST"])
@login_required
@admin_required
def adjust_stock(barcode):
    product = Product.query.filter(Product.barcode == barcode).first_or_404()
    qty = request.form.get("quantity", type=int)
    reason = request.form.get("reason", "").strip()
    if qty is None or qty == 0:
        flash(notify_warning("Quantity change must be non-zero"))
        return redirect(url_for("product.edit_dashboard", barcode=barcode))
    if not reason:
        flash(notify_warning("Reason is required"))
        return redirect(url_for("product.edit_dashboard", barcode=barcode))
    product.in_stock += qty
    product.log_adjustment(qty, reason, "Manual adjustment")
    product.update()
    flash(notify_success(f"Stock adjusted by {qty}. New stock: {product.in_stock}"))
    return redirect(url_for("product.edit_dashboard", barcode=barcode))


@module_blueprint.route("/<barcode>/bundle/add", methods=["POST"])
@login_required
@admin_required
def bundle_add_component(barcode):
    product = Product.query.filter_by(barcode=barcode).first_or_404()
    comp_barcode = request.form.get("component_barcode", "").strip()
    qty = request.form.get("quantity", 1, type=int)
    comp = Product.query.filter_by(barcode=comp_barcode).first()
    if not comp:
        flash(notify_warning("Component product not found"))
        return redirect(url_for("product.edit_dashboard", barcode=barcode))
    BundleComponent(bundle_product_id=product.id, component_product_id=comp.id, quantity=qty).insert()
    flash(notify_success(f"Added {comp.name} x{qty} to bundle"))
    return redirect(url_for("product.edit_dashboard", barcode=barcode))


@module_blueprint.route("/bundle/<int:bc_id>/remove", methods=["POST"])
@login_required
@admin_required
def bundle_remove_component(bc_id):
    bc = BundleComponent.query.get_or_404(bc_id)
    barcode = bc.component.barcode if bc.component else ""
    bc.delete()
    flash(notify_success("Component removed"))
    return redirect(url_for("product.edit_dashboard", barcode=barcode))


@module_blueprint.route("/labels")
@login_required
@admin_required
def labels():
    products = Product.query.order_by(Product.name).all()
    return render_template("product/labels.html", **products)
