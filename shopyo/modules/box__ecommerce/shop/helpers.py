import json
import os

from flask import session

from shopyoapi.enhance import get_setting

from modules.box__ecommerce.product.models import Product

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
    if "cart" in session:
        cart_data = session["cart"][0]
        cart_items = sum(cart_data.values())

        cart_total_price = 0
        try:
            for item in cart_data:
                print(item)
                product = Product.query.get(item)
                cart_total_price += (
                    int(cart_data[item]) * product.selling_price
                )
        except Exception as e:
            pass

    else:
        session["cart"] = [{}]
        cart_data = session["cart"][0]
        cart_items = 0
        cart_total_price = 0

    return {
        "cart_data": cart_data,
        "cart_items": cart_items,
        "cart_total_price": cart_total_price,
    }
