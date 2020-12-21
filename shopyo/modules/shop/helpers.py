from flask import session

from modules.product.models import Product


def get_cart_data():
    if "cart" in session:
        cart_data = session["cart"][0]
        cart_items = sum(cart_data.values())

        cart_total_price = 0
        try:
            for item in cart_data:
                print(item)
                product = Product.query.get(item)
                cart_total_price += int(cart_data[item]) * product.selling_price
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
