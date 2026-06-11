from flask import flash, redirect, request, url_for
from flask_login import login_required
from shopyo.api.html import notify_success, notify_warning
from shopyo.api.forms import flash_errors
from shopyo.api.module import ModuleHelp
from shopyo_appadmin.admin import admin_required
from sqlalchemy import and_

from init import db
from modules.box__ecommerce.product.models import Product
from .models import InventoryCount, InventoryCountItem
from .forms import InventoryCountForm

mhelp = ModuleHelp(__file__, __name__)
globals()[mhelp.blueprint_str] = mhelp.blueprint
module_blueprint = globals()[mhelp.blueprint_str]


@module_blueprint.route(mhelp.info["dashboard"])
@login_required
@admin_required
def dashboard():
    context = mhelp.context()
    counts = InventoryCount.query.order_by(InventoryCount.created_at.desc()).all()
    context.update({"counts": counts})
    return mhelp.render("dashboard.html", **context)


@module_blueprint.route("/new", methods=["GET", "POST"])
@login_required
@admin_required
def new():
    form = InventoryCountForm()
    if request.method == "POST" and form.validate_on_submit():
        count = InventoryCount(notes=form.notes.data or "")
        for p in Product.query.order_by(Product.name).all():
            count.items.append(InventoryCountItem(product_id=p.id, expected_qty=p.in_stock or 0))
        count.insert()
        flash(notify_success(f"Count sheet #{count.id} created with {len(count.items)} items"))
        return redirect(url_for("inventory.count", count_id=count.id))
    context = mhelp.context()
    context.update({"form": form})
    return mhelp.render("new.html", **context)


@module_blueprint.route("/<count_id>", methods=["GET", "POST"])
@login_required
@admin_required
def count(count_id):
    c = InventoryCount.query.get_or_404(count_id)
    if request.method == "POST":
        for item in c.items:
            qty = request.form.get(f"qty_{item.id}", type=int)
            if qty is not None:
                item.actual_qty = qty
        c.status = "completed"
        db.session.commit()
        for item in c.items:
            if item.variance != 0:
                prod = Product.query.get(item.product_id)
                if prod:
                    prod.in_stock = item.actual_qty
                    prod.log_adjustment(item.variance, "inventory count", f"Count #{c.id}")
        c.status = "reviewed"
        c.update()
        flash(notify_success(f"Count #{c.id} completed. Variances applied."))
        return redirect(url_for("inventory.dashboard"))
    context = mhelp.context()
    context.update({"count": c})
    return mhelp.render("count.html", **context)


@module_blueprint.route("/<count_id>/delete", methods=["POST"])
@login_required
@admin_required
def delete(count_id):
    c = InventoryCount.query.get_or_404(count_id)
    db.session.delete(c)
    db.session.commit()
    flash(notify_success(f"Count #{count_id} deleted"))
    return redirect(url_for("inventory.dashboard"))


@module_blueprint.route("/reports")
@login_required
@admin_required
def reports():
    context = mhelp.context()
    products = Product.query.order_by(Product.name).all()
    total_cost = sum(float(p.cost_price or 0) * (p.in_stock or 0) for p in products)
    total_retail = sum(float(p.selling_price or 0) * (p.in_stock or 0) for p in products)
    low_stock = [p for p in products if p.min_stock and p.in_stock and p.in_stock <= p.min_stock]
    out_of_stock = [p for p in products if not p.in_stock or p.in_stock == 0]
    context.update({"products": products, "total_cost": total_cost, "total_retail": total_retail,
                     "low_stock": low_stock, "out_of_stock": out_of_stock})
    return mhelp.render("reports.html", **context)
