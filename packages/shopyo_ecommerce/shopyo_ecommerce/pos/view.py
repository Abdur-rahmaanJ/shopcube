from datetime import datetime, timedelta
from functools import wraps

from flask import jsonify
from flask import render_template
from flask import request

from flask import flash, redirect, url_for
from flask_login import current_user, login_required
from shopyo.api.html import notify_success, notify_warning
from shopyo.api.module import ModuleHelp
from shopyo_appadmin.admin import admin_required
from shopyo_auth.decorators import check_confirmed
from sqlalchemy.orm import subqueryload

from init import db
from shopyo_ecommerce.category.models import Category, SubCategory
from shopyo_ecommerce.inventory.models import Location, StockPerLocation
from shopyo_ecommerce.pos.models import Transaction, TransactionItem
from shopyo_ecommerce.pos.models import Shift
from shopyo_ecommerce.pos.models import QuickKey
from shopyo_ecommerce.product.models import Product
from shopyo_ecommerce._utils import get_currency_symbol
from shopyo_settings.helpers import get_setting
mhelp = ModuleHelp(__file__, __name__)
globals()[mhelp.blueprint_str] = mhelp.blueprint
module_blueprint = globals()[mhelp.blueprint_str]


def pos_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if current_user.is_admin:
            return f(*args, **kwargs)
        if any(r.name == "cashier" for r in current_user.roles):
            return f(*args, **kwargs)
        return redirect("/")
    return wrap


@module_blueprint.route("/")
@login_required
@check_confirmed
@pos_required
def index():
    context = mhelp.context()
    

    categories = Category.query.all()
    quick_keys = QuickKey.query.order_by(QuickKey.position).all()
    locations = Location.query.filter_by(is_active=True).all()
    if not locations:
        loc = Location(name="Main Store", address="Default", is_active=True)
        loc.insert()
        locations = [loc]
    context.update({
        "categories": categories,
        "quick_keys": quick_keys,
        "locations": locations,
        "store_name": get_setting("STORE_NAME") or "",
        "store_tel": get_setting("STORE_TEL") or "",
        "currency_symbol": get_currency_symbol(),
    })
    return render_template("pos/index.html", **context)


@module_blueprint.route("/transaction", methods=["POST"])
@login_required
@check_confirmed
@pos_required
def transaction():
    data = request.get_json()
    if not data or "items" not in data:
        return jsonify({"success": False, "message": "Invalid request data"}), 400

    items_data = data["items"]
    amount_paid = data.get("amount_paid")
    payment_method = data.get("payment_method", "")
    notes = data.get("notes", "")
    discount_type = data.get("discount_type", "")
    discount_value = data.get("discount_value", 0)
    location_id = data.get("location_id")
    card_last_four = data.get("card_last_four", "")
    card_auth_code = data.get("card_auth_code", "")

    if amount_paid is None or not isinstance(amount_paid, (int, float)) or amount_paid < 0:
        return jsonify({"success": False, "message": "Invalid or missing amount paid"}), 400

    errors = []
    computed_total = 0
    for barcode, item_data in items_data.items():
        quantity = float(item_data.get("count", 0))
        if quantity < 0.01:
            errors.append(f"Invalid quantity for barcode {barcode}")
            continue
        product = Product.query.filter_by(barcode=str(barcode)).first()
        if product is None:
            errors.append(f"Product not found: {barcode}")
        elif not product.is_variable_qty and quantity != int(quantity):
            errors.append(f"Quantity must be whole number for {product.name}")
        elif not product.is_variable_qty and int(quantity) > product.in_stock:
            errors.append(
                f"Insufficient stock for {product.name}: "
                f"requested {int(quantity)}, available {product.in_stock}"
            )
        else:
            unit_price = float(item_data.get("unit_price", product.selling_price))
            computed_total += unit_price * quantity

    if errors:
        return jsonify({"success": False, "message": "; ".join(errors)}), 400

    computed_total = float(computed_total)

    discount_amount = 0
    if discount_type == "percentage":
        pct = min(float(discount_value), 100)
        discount_amount = computed_total * (pct / 100)
    elif discount_type == "fixed":
        discount_amount = min(float(discount_value), computed_total)

    net_total = computed_total - discount_amount

    if amount_paid < net_total:
        return jsonify({
            "success": False,
            "message": f"Insufficient payment. Total: ${net_total:.2f}, Received: ${amount_paid:.2f}"
        }), 400

    transaction = Transaction()
    transaction.cashier_id = current_user.id
    transaction.total_amount = computed_total
    transaction.method_of_payment = payment_method
    transaction.notes = notes
    transaction.discount_type = discount_type
    transaction.discount_value = discount_value
    transaction.location_id = location_id
    transaction.card_last_four = card_last_four or None
    transaction.card_auth_code = card_auth_code or None

    for barcode, item_data in items_data.items():
        quantity = float(item_data["count"])
        product = Product.query.filter_by(barcode=str(barcode)).first()
        deduct = int(quantity) if not product.is_variable_qty else int(quantity)
        product.in_stock -= deduct
        if location_id:
            current = product.stock_at(location_id)
            product.set_stock(location_id, current - deduct)
        product.log_adjustment(-deduct, "POS sale", f"Transaction via {payment_method}")
        unit_price = float(item_data.get("unit_price", product.selling_price))
        item = TransactionItem(
            product_barcode=barcode,
            quantity=quantity,
            unit_price=unit_price,
        )
        transaction.items.append(item)

    db.session.add(transaction)
    db.session.commit()

    receipt_items = []
    for item in transaction.items:
        product = Product.query.filter_by(barcode=item.product_barcode).first()
        receipt_items.append({
            "barcode": item.product_barcode,
            "name": product.name if product else item.product_barcode,
            "qty": item.quantity,
            "unit_price": float(item.unit_price),
            "subtotal": float(item.quantity * item.unit_price),
        })

    return jsonify({
        "success": True,
        "message": "Transaction completed successfully",
        "tx": {
            "id": transaction.id,
            "time": transaction.time.strftime("%Y-%m-%d %H:%M"),
            "total": float(transaction.total_amount),
            "discount_type": transaction.discount_type or "",
            "discount_value": float(transaction.discount_value or 0),
            "net_total": round(net_total, 2),
            "method": transaction.method_of_payment,
            "amount_paid": float(amount_paid),
            "change": round(float(amount_paid) - net_total, 2),
            "card_last_four": transaction.card_last_four,
            "items": receipt_items,
        }
    })


@module_blueprint.route("/reports/dashboard")
@login_required
@admin_required
def reports():
    context = mhelp.context()
    days = request.args.get("days", 7, type=int)
    since = datetime.now() - timedelta(days=days)
    txs = Transaction.query.filter(Transaction.time >= since).order_by(Transaction.time.desc()).all()
    total_sales = sum(float(t.total_amount or 0) for t in txs)
    total_tx = len(txs)
    by_method = {}
    by_cashier = {}
    by_location = {}
    for t in txs:
        m = t.method_of_payment or "unknown"
        by_method[m] = by_method.get(m, 0) + float(t.total_amount or 0)
        c = t.cashier_id or 0
        by_cashier[c] = by_cashier.get(c, 0) + 1
        loc_id = t.location_id or 0
        by_location[loc_id] = by_location.get(loc_id, 0) + float(t.total_amount or 0)
    context.update({"txs": txs, "total_sales": total_sales, "total_tx": total_tx,
                     "by_method": by_method, "by_cashier": by_cashier, "by_location": by_location, "days": days,
                     "currency_symbol": get_currency_symbol()})
    return mhelp.render("reports.html", **context)


@module_blueprint.route("/return", methods=["GET", "POST"])
@login_required
@admin_required
def returns():
    context = mhelp.context()
    tx = None
    if request.method == "POST":
        receipt_id = request.form.get("receipt_id", type=int)
        tx = Transaction.query.get(receipt_id)
        if not tx:
            flash("Transaction not found", "warning")
    context["tx"] = tx
    context["currency_symbol"] = get_currency_symbol()
    return mhelp.render("return.html", **context)


@module_blueprint.route("/return/<int:tx_id>/process", methods=["POST"])
@login_required
@admin_required
def process_return(tx_id):
    tx = Transaction.query.get_or_404(tx_id)
    refund_tx = Transaction(
        cashier_id=current_user.id,
        total_amount=-float(tx.total_amount or 0),
        method_of_payment="refund",
        notes=f"Return of transaction #{tx.id}",
    )
    refund_tx.insert()
    for item in tx.items:
        product = Product.query.filter_by(barcode=item.product_barcode).first()
        if product:
            product.in_stock = (product.in_stock or 0) + int(item.quantity)
            product.log_adjustment(int(item.quantity), "return", f"Return of TX #{tx.id}")
    flash(f"Return processed. Refund: ${float(tx.total_amount or 0):.2f}", "success")
    return redirect(url_for("shopyo_ecommerce.pos.returns"))


@module_blueprint.route("/shifts/dashboard")
@login_required
@admin_required
def shifts():
    context = mhelp.context()
    context["shifts"] = Shift.query.order_by(Shift.opened_at.desc()).all()
    active = Shift.query.filter_by(status="open").first()
    context["active_shift"] = active
    context["currency_symbol"] = get_currency_symbol()
    return mhelp.render("shifts.html", **context)


@module_blueprint.route("/shift/open", methods=["POST"])
@login_required
@admin_required
def shift_open():
    if Shift.query.filter_by(status="open").first():
        flash("A shift is already open", "warning")
        return redirect(url_for("shopyo_ecommerce.pos.shifts"))
    s = Shift(user_id=current_user.id, starting_cash=request.form.get("starting_cash", 0, type=float))
    s.insert()
    flash("Shift opened", "success")
    return redirect(url_for("shopyo_ecommerce.pos.shifts"))


@module_blueprint.route("/shift/<int:shift_id>/close", methods=["POST"])
@login_required
@admin_required
def shift_close(shift_id):
    s = Shift.query.get_or_404(shift_id)
    if s.status != "open":
        flash("Shift already closed", "warning")
        return redirect(url_for("shopyo_ecommerce.pos.shifts"))
    actual = request.form.get("actual_cash", 0, type=float)
    s.actual_cash = actual
    s.closed_at = datetime.now()
    s.expected_cash = float(s.starting_cash) + s.total_sales()
    s.variance_cash = actual - float(s.expected_cash)
    s.status = "closed"
    s.update()
    flash(f"Shift closed. Variance: ${float(s.variance_cash):.2f}", "success")
    return redirect(url_for("shopyo_ecommerce.pos.shifts"))


@module_blueprint.route("/quick-keys/dashboard")
@login_required
@admin_required
def quick_keys():
    context = mhelp.context()
    keys = QuickKey.query.order_by(QuickKey.position).all()
    products = Product.query.filter_by(discontinued=False).order_by(Product.name).all()
    context.update({"keys": keys, "products": products})
    return mhelp.render("quick_keys.html", **context)


@module_blueprint.route("/quick-keys/add", methods=["POST"])
@login_required
@admin_required
def quick_key_add():
    product_id = request.form.get("product_id", type=int)
    position = request.form.get("position", type=int)
    label = request.form.get("label", "").strip()
    if not product_id or position is None:
        flash("Product and position are required", "warning")
        return redirect(url_for("shopyo_ecommerce.pos.quick_keys"))
    existing = QuickKey.query.filter_by(position=position).first()
    if existing:
        existing.product_id = product_id
        existing.label = label or None
        existing.update()
    else:
        qk = QuickKey(product_id=product_id, position=position, label=label or None)
        qk.insert()
    flash("Quick key saved", "success")
    return redirect(url_for("shopyo_ecommerce.pos.quick_keys"))


@module_blueprint.route("/quick-keys/<int:key_id>/delete", methods=["POST"])
@login_required
@admin_required
def quick_key_delete(key_id):
    qk = QuickKey.query.get_or_404(key_id)
    qk.delete()
    flash("Quick key removed", "success")
    return redirect(url_for("shopyo_ecommerce.pos.quick_keys"))


@module_blueprint.route("/transactions/dashboard")
@login_required
@admin_required
def transactions_list():
    page = request.args.get("page", 1, type=int)
    q = request.args.get("q", "", type=str)
    query = Transaction.query
    if q:
        query = query.filter(Transaction.id == int(q)) if q.isdigit() else query
    txs = query.order_by(Transaction.time.desc()).paginate(page=page, per_page=25, error_out=False)
    context = mhelp.context()
    context.update({"txs": txs, "q": q, "currency_symbol": get_currency_symbol()})
    return mhelp.render("transactions.html", **context)


@module_blueprint.route("/transactions/<int:tx_id>/view")
@login_required
@admin_required
def transaction_view(tx_id):
    tx = Transaction.query.get_or_404(tx_id)
    context = mhelp.context()
    context.update({"tx": tx, "currency_symbol": get_currency_symbol()})
    return mhelp.render("transaction_view.html", **context)
