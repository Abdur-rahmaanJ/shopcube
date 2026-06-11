from datetime import datetime, timedelta

from flask import jsonify
from flask import render_template
from flask import request

from flask_login import current_user
from flask_login import login_required
from shopyo.api.module import ModuleHelp
from shopyo_appadmin.admin import admin_required
from shopyo_auth.decorators import check_confirmed
from sqlalchemy.orm import subqueryload

from init import db
from modules.box__ecommerce.category.models import Category, SubCategory
from modules.box__ecommerce.pos.models import Transaction, TransactionItem
from modules.box__ecommerce.product.models import Product

mhelp = ModuleHelp(__file__, __name__)
globals()[mhelp.blueprint_str] = mhelp.blueprint
module_blueprint = globals()[mhelp.blueprint_str]


@module_blueprint.route("/")
@login_required
@check_confirmed
@admin_required
def index():
    context = mhelp.context()
    categories = Category.query.options(
        subqueryload(Category.subcategories).subqueryload(SubCategory.products)
    ).all()
    context.update({"categories": categories})
    return render_template("pos/index.html", **context)


@module_blueprint.route("/transaction", methods=["POST"])
@login_required
@check_confirmed
@admin_required
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

    if amount_paid is None or not isinstance(amount_paid, (int, float)) or amount_paid < 0:
        return jsonify({"success": False, "message": "Invalid or missing amount paid"}), 400

    errors = []
    computed_total = 0
    for barcode, item_data in items_data.items():
        quantity = item_data.get("count", 0)
        if not isinstance(quantity, int) or quantity < 1:
            errors.append(f"Invalid quantity for barcode {barcode}")
            continue
        product = Product.query.filter_by(barcode=str(barcode)).first()
        if product is None:
            errors.append(f"Product not found: {barcode}")
        elif quantity > product.in_stock:
            errors.append(
                f"Insufficient stock for {product.name}: "
                f"requested {quantity}, available {product.in_stock}"
            )
        else:
            computed_total += product.selling_price * quantity

    if errors:
        return jsonify({"success": False, "message": "; ".join(errors)}), 400

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

    for barcode, item_data in items_data.items():
        quantity = item_data["count"]
        product = Product.query.filter_by(barcode=str(barcode)).first()
        product.in_stock -= quantity
        product.log_adjustment(-quantity, "POS sale", f"Transaction via {payment_method}")
        item = TransactionItem(
            product_barcode=barcode,
            quantity=quantity,
            unit_price=product.selling_price,
        )
        transaction.items.append(item)

    db.session.add(transaction)
    db.session.commit()

    return jsonify({"success": True, "message": "Transaction completed successfully"})


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
    for t in txs:
        m = t.method_of_payment or "unknown"
        by_method[m] = by_method.get(m, 0) + float(t.total_amount or 0)
    context.update({"txs": txs, "total_sales": total_sales, "total_tx": total_tx, "by_method": by_method, "days": days})
    return mhelp.render("reports.html", **context)
