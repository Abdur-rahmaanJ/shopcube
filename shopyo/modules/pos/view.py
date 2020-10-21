import os
import json

from flask import Blueprint
from flask import render_template

# from flask import url_for
# from flask import redirect
# from flask import flash

from flask import request
from flask import jsonify

from shopyoapi.enhance import base_context

# from shopyoapi.html import notify_success
# from shopyoapi.forms import flash_errors


from modules.category.models import Category
from modules.product.models import Product
from modules.pos.models import Transaction

from flask_login import current_user
from flask_login import login_required

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


@login_required
@module_blueprint.route("/")
def index():
    context = base_context()
    categories = Category.query.all()
    context.update({"categories": categories})
    return render_template("pos/index.html", **context)


@login_required
@module_blueprint.route("/transaction", methods=["GET", "POST"])
def transaction():
    if request.method == "POST":
        json = request.get_json()
        for key in json:
            prod_id = key
            number_items = json[key]["count"]
            product = Product.query.get(prod_id)
            product.in_stock -= number_items

            product.update()

        transaction = Transaction()
        transaction.cashier_id = current_user.id
        transaction.products = [Product.query.get(key) for key in json]
        transaction.insert()

    return jsonify({"message": "ok"})
