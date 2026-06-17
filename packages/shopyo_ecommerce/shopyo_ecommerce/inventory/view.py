from flask import flash, redirect, request, url_for
from flask_login import login_required
from shopyo.api.html import notify_success, notify_warning
from shopyo.api.forms import flash_errors
from shopyo.api.module import ModuleHelp
from shopyo_appadmin.admin import admin_required
from sqlalchemy import and_

from init import db
from shopyo_ecommerce.product.models import Product
from .models import InventoryCount, InventoryCountItem
from .models import Location, StockPerLocation, StockTransfer, StockTransferItem
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
        return redirect(url_for("shopyo_ecommerce.inventory.count", count_id=count.id))
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
        return redirect(url_for("shopyo_ecommerce.inventory.dashboard"))
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
    return redirect(url_for("shopyo_ecommerce.inventory.dashboard"))


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


# --- Locations ---


@module_blueprint.route("/locations")
@login_required
@admin_required
def locations():
    context = mhelp.context()
    context["locations"] = Location.query.order_by(Location.name).all()
    return mhelp.render("locations.html", **context)


@module_blueprint.route("/locations/add", methods=["POST"])
@login_required
@admin_required
def location_add():
    name = request.form.get("name", "").strip()
    address = request.form.get("address", "").strip()
    if name:
        Location(name=name, address=address).insert()
        flash(notify_success(f"Location '{name}' added"))
    return redirect(url_for("shopyo_ecommerce.inventory.locations"))


@module_blueprint.route("/locations/<int:loc_id>/delete", methods=["POST"])
@login_required
@admin_required
def location_delete(loc_id):
    loc = Location.query.get_or_404(loc_id)
    loc.delete()
    flash(notify_success("Location deleted"))
    return redirect(url_for("shopyo_ecommerce.inventory.locations"))


@module_blueprint.route("/locations/<int:loc_id>/stock")
@login_required
@admin_required
def location_stock(loc_id):
    context = mhelp.context()
    loc = Location.query.get_or_404(loc_id)
    products = Product.query.order_by(Product.name).all()
    stock_data = []
    for p in products:
        spl = StockPerLocation.query.filter_by(product_id=p.id, location_id=loc_id).first()
        stock_data.append({"product": p, "qty": spl.quantity if spl else 0})
    context.update({"loc": loc, "stock_data": stock_data})
    return mhelp.render("location_stock.html", **context)


@module_blueprint.route("/locations/<int:loc_id>/stock/update", methods=["POST"])
@login_required
@admin_required
def location_stock_update(loc_id):
    from shopyo_ecommerce.product.models import Product as Prod
    for key, value in request.form.items():
        if key.startswith("qty_"):
            pid = int(key.replace("qty_", ""))
            qty = int(value) if value else 0
            prod = Prod.query.get(pid)
            if prod:
                old = prod.stock_at(loc_id)
                prod.set_stock(loc_id, qty)
                diff = qty - old
                if diff != 0:
                    prod.log_adjustment(diff, "location stock edit", f"Location #{loc_id}")
    flash(notify_success("Stock updated"))
    return redirect(url_for("shopyo_ecommerce.inventory.location_stock", loc_id=loc_id))


# --- Stock Transfers ---


@module_blueprint.route("/transfers")
@login_required
@admin_required
def transfers():
    context = mhelp.context()
    context["transfers"] = StockTransfer.query.order_by(StockTransfer.created_at.desc()).all()
    context["locations"] = Location.query.filter_by(is_active=True).all()
    context["products"] = Product.query.order_by(Product.name).all()
    return mhelp.render("transfers.html", **context)


@module_blueprint.route("/transfers/create", methods=["POST"])
@login_required
@admin_required
def transfer_create():
    from_id = request.form.get("from_location_id", type=int)
    to_id = request.form.get("to_location_id", type=int)
    if not from_id or not to_id or from_id == to_id:
        flash(notify_warning("Select two different locations"))
        return redirect(url_for("shopyo_ecommerce.inventory.transfers"))
    t = StockTransfer(from_location_id=from_id, to_location_id=to_id)
    t.insert()
    flash(notify_success("Transfer created. Add items."))
    return redirect(url_for("shopyo_ecommerce.inventory.transfers"))


@module_blueprint.route("/transfers/<int:t_id>/add-item", methods=["POST"])
@login_required
@admin_required
def transfer_add_item(t_id):
    t = StockTransfer.query.get_or_404(t_id)
    if t.status != "draft":
        flash(notify_warning("Cannot modify a non-draft transfer"))
        return redirect(url_for("shopyo_ecommerce.inventory.transfers"))
    product_id = request.form.get("product_id", type=int)
    qty = request.form.get("quantity", 0, type=int)
    if not product_id or qty < 1:
        flash(notify_warning("Invalid product or quantity"))
        return redirect(url_for("shopyo_ecommerce.inventory.transfers"))
    StockTransferItem(transfer_id=t_id, product_id=product_id, quantity=qty).insert()
    flash(notify_success("Item added"))
    return redirect(url_for("shopyo_ecommerce.inventory.transfers"))


@module_blueprint.route("/transfers/<int:t_id>/complete", methods=["POST"])
@login_required
@admin_required
def transfer_complete(t_id):
    t = StockTransfer.query.get_or_404(t_id)
    if t.status != "draft":
        flash(notify_warning("Already completed"))
        return redirect(url_for("shopyo_ecommerce.inventory.transfers"))
    for item in t.items:
        prod = Product.query.get(item.product_id)
        if prod:
            prod.in_stock = (prod.in_stock or 0) - item.quantity
            prod.log_adjustment(-item.quantity, "stock transfer out", f"Transfer #{t.id}")
    t.status = "completed"
    t.update()
    flash(notify_success("Transfer completed. Stock deducted from source."))
    return redirect(url_for("shopyo_ecommerce.inventory.transfers"))


@module_blueprint.route("/transfers/<int:t_id>/receive", methods=["POST"])
@login_required
@admin_required
def transfer_receive(t_id):
    t = StockTransfer.query.get_or_404(t_id)
    if t.status != "completed":
        flash(notify_warning("Transfer must be completed first"))
        return redirect(url_for("shopyo_ecommerce.inventory.transfers"))
    for item in t.items:
        prod = Product.query.get(item.product_id)
        if prod:
            prod.in_stock = (prod.in_stock or 0) + item.quantity
            prod.log_adjustment(item.quantity, "stock transfer in", f"Transfer #{t.id}")
    t.status = "received"
    t.update()
    flash(notify_success("Transfer received. Stock added to destination."))
    return redirect(url_for("shopyo_ecommerce.inventory.transfers"))
