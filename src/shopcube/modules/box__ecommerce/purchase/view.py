from flask import flash, jsonify, redirect, render_template, request, url_for
from flask_login import login_required
from shopyo.api.html import notify_success, notify_warning
from shopyo.api.forms import flash_errors
from shopyo.api.module import ModuleHelp
from shopyo_appadmin.admin import admin_required

from init import db
from modules.box__ecommerce.vendor.models import Vendor
from modules.box__ecommerce.product.models import Product
from .models import PurchaseOrder, PurchaseOrderItem
from .forms import PurchaseOrderForm

mhelp = ModuleHelp(__file__, __name__)
globals()[mhelp.blueprint_str] = mhelp.blueprint
module_blueprint = globals()[mhelp.blueprint_str]


@module_blueprint.route(mhelp.info["dashboard"])
@login_required
@admin_required
def dashboard():
    context = mhelp.context()
    orders = PurchaseOrder.query.order_by(PurchaseOrder.created_at.desc()).all()
    context.update({"orders": orders})
    return mhelp.render("dashboard.html", **context)


@module_blueprint.route("/add", methods=["GET", "POST"])
@login_required
@admin_required
def add():
    form = PurchaseOrderForm()
    form.vendor_id.choices = [(0, "-- None --")] + [(v.id, v.name) for v in Vendor.query.order_by(Vendor.name).all()]
    if request.method == "POST" and form.validate_on_submit():
        po = PurchaseOrder(
            vendor_id=form.vendor_id.data if form.vendor_id.data else None,
            notes=form.notes.data.strip() if form.notes.data else "",
        )
        po.insert()
        flash(notify_success(f"Purchase Order #{po.id} created"))
        return redirect(url_for("purchase.edit", po_id=po.id))
    context = mhelp.context()
    context.update({"form": form})
    return mhelp.render("add.html", **context)


@module_blueprint.route("/<po_id>/edit", methods=["GET", "POST"])
@login_required
@admin_required
def edit(po_id):
    po = PurchaseOrder.query.get_or_404(po_id)
    form = PurchaseOrderForm(obj=po)
    form.vendor_id.choices = [(0, "-- None --")] + [(v.id, v.name) for v in Vendor.query.order_by(Vendor.name).all()]
    if request.method == "POST":
        if form.validate_on_submit():
            po.vendor_id = form.vendor_id.data if form.vendor_id.data else None
            po.notes = form.notes.data.strip() if form.notes.data else ""
            po.update()
            flash(notify_success(f"PO #{po.id} updated"))
            return redirect(url_for("purchase.edit", po_id=po.id))
        else:
            flash_errors(form)
    context = mhelp.context()
    context.update({"po": po, "form": form})
    return mhelp.render("edit.html", **context)


@module_blueprint.route("/<po_id>/item/add", methods=["POST"])
@login_required
@admin_required
def add_item(po_id):
    po = PurchaseOrder.query.get_or_404(po_id)
    if po.status not in ("draft",):
        flash(notify_warning("Cannot modify a non-draft order"))
        return redirect(url_for("purchase.edit", po_id=po_id))
    barcode = request.form.get("barcode", "").strip()
    qty = request.form.get("quantity", 1, type=int)
    if not barcode:
        flash(notify_warning("Barcode is required"))
        return redirect(url_for("purchase.edit", po_id=po_id))
    product = Product.query.filter_by(barcode=barcode).first()
    item = PurchaseOrderItem(
        product_barcode=barcode,
        product_name=product.name if product else barcode,
        quantity_ordered=qty,
        unit_price=product.price if product else 0,
    )
    po.items.append(item)
    po.update()
    flash(notify_success(f"Added {item.product_name} x{qty}"))
    return redirect(url_for("purchase.edit", po_id=po_id))


@module_blueprint.route("/item/<item_id>/delete", methods=["POST"])
@login_required
@admin_required
def delete_item(item_id):
    item = PurchaseOrderItem.query.get_or_404(item_id)
    po_id = item.purchase_order_id
    po = PurchaseOrder.query.get(po_id)
    if po and po.status != "draft":
        flash(notify_warning("Cannot modify a non-draft order"))
        return redirect(url_for("purchase.edit", po_id=po_id))
    db.session.delete(item)
    db.session.commit()
    flash(notify_success("Item removed"))
    return redirect(url_for("purchase.edit", po_id=po_id))


@module_blueprint.route("/<po_id>/receive", methods=["POST"])
@login_required
@admin_required
def receive(po_id):
    po = PurchaseOrder.query.get_or_404(po_id)
    if po.status != "ordered":
        flash(notify_warning("Only ordered POs can be received"))
        return redirect(url_for("purchase.edit", po_id=po_id))
    for item in po.items:
        qty = request.form.get(f"qty_received_{item.id}", item.quantity_ordered, type=int)
        item.quantity_received = qty
        product = Product.query.filter_by(barcode=item.product_barcode).first()
        if product:
            product.in_stock = (product.in_stock or 0) + qty
            product.log_adjustment(qty, "PO receive", f"PO #{po.id}")
    po.status = "received"
    po.update()
    flash(notify_success(f"PO #{po.id} received"))
    return redirect(url_for("purchase.edit", po_id=po_id))


@module_blueprint.route("/<po_id>/order", methods=["POST"])
@login_required
@admin_required
def place_order(po_id):
    po = PurchaseOrder.query.get_or_404(po_id)
    if po.status != "draft":
        flash(notify_warning("Only draft POs can be ordered"))
        return redirect(url_for("purchase.edit", po_id=po_id))
    if not po.items:
        flash(notify_warning("Cannot order a PO with no items"))
        return redirect(url_for("purchase.edit", po_id=po_id))
    po.status = "ordered"
    po.update()
    flash(notify_success(f"PO #{po.id} placed"))
    return redirect(url_for("purchase.edit", po_id=po_id))


@module_blueprint.route("/<po_id>/delete", methods=["POST"])
@login_required
@admin_required
def delete(po_id):
    po = PurchaseOrder.query.get_or_404(po_id)
    if po.status not in ("draft", "cancelled"):
        flash(notify_warning("Only draft/cancelled POs can be deleted"))
        return redirect(url_for("purchase.dashboard"))
    db.session.delete(po)
    db.session.commit()
    flash(notify_success(f"PO #{po_id} deleted"))
    return redirect(url_for("purchase.dashboard"))


@module_blueprint.route("/product/<barcode>/info", methods=["GET"])
@login_required
@admin_required
def product_info(barcode):
    product = Product.query.filter_by(barcode=barcode).first()
    if product:
        return jsonify({
            "name": product.name,
            "price": float(product.price or 0),
            "in_stock": product.in_stock or 0,
        })
    return jsonify({"name": barcode, "price": 0, "in_stock": 0})
