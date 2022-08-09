import json
import os
from flask import session
from modules.box__ecommerce.product.models import Product
from modules.box__ecommerce.category.models import Category
from modules.box__ecommerce.category.models import SubCategory
from modules.box__default.settings.helpers import get_setting
from utils.session import Cart

dirpath = os.path.dirname(os.path.abspath(__file__))
box_path = os.path.dirname(dirpath)


def get_currency_symbol():
    curr_code = get_setting("CURRENCY")
    with open(
        os.path.join(
            box_path,
            "shopman",
            "data",
            "currency.json",
        )
    ) as f:
        currencies = json.load(f)
    for curr in currencies:
        if curr["cc"] == curr_code:
            return curr["symbol"]


def get_cart_data():
    cart_data = Cart.data()
    return {
        'cart_items': cart_data['num_items'],
        'cart_total_price': cart_data['total_price'],
        'cart_data': cart_data['items']
        }


def get_min_max_subcateg(subcategory_name):
    subcateg = SubCategory.query.filter(SubCategory.name == subcategory_name).first()
    if len(subcateg.products) > 0:
        min_price = min((p.selling_price for p in subcateg.products))
        max_price = max((p.selling_price for p in subcateg.products))
    else:
        min_price = 0
        max_price = 2000
    return [min_price, max_price]