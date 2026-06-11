from flask import jsonify
from flask import render_template
from flask import request

from flask_login import current_user
from flask_login import login_required
from shopyo.api.module import ModuleHelp
from shopyo_appadmin.admin import admin_required
from shopyo_auth.decorators import check_confirmed

from init import db
from modules.box__ecommerce.category.models import Category
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
    categories = Category.query.all()
    context.update({"categories": categories})
    return render_template("pos/index.html", **context)


@module_blueprint.route("/transaction", methods=["POST"])
@login_required
@check_confirmed
@admin_required
def transaction():
    data = request.get_json()
    if not data:
        return jsonify({"success": False, "message": "No data provided"}), 400

    errors = []
    for barcode, item_data in data.items():
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

    if errors:
        return jsonify({"success": False, "message": "; ".join(errors)}), 400

    transaction = Transaction()
    transaction.cashier_id = current_user.id
    transaction.total_amount = 0

    for barcode, item_data in data.items():
        quantity = item_data["count"]
        product = Product.query.filter_by(barcode=str(barcode)).first()
        product.in_stock -= quantity
        item = TransactionItem(
            product_barcode=barcode,
            quantity=quantity,
            unit_price=product.selling_price,
        )
        transaction.items.append(item)
        transaction.total_amount += product.selling_price * quantity

    db.session.add(transaction)
    db.session.commit()

    return jsonify({"success": True, "message": "Transaction completed successfully"})
