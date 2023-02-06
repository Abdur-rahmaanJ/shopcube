from flask import session

from utils.session import Cart

from modules.box__ecommerce.shop.helpers import get_cart_data
from modules.box__ecommerce.shop.helpers import get_currency_symbol
from modules.box__ecommerce.shop.helpers import get_min_max_subcateg


from .forms import LoginForm
from .forms import RegisterCustomerForm


def get_auth_login_form():
    return LoginForm()


def get_auth_register_customer_form():
    return RegisterCustomerForm()

def get_wishlist_data():
    if "wishlist" not in session:
        session["wishlist"] = []
        return session["wishlist"]

    return session["wishlist"]


available_everywhere = {
    "get_currency_symbol": get_currency_symbol,
    "get_min_max_subcateg": get_min_max_subcateg,
    "get_wishlist_data": get_wishlist_data,
    "get_cart_data": get_cart_data,
    "Cart": Cart,
    "get_auth_login_form": get_auth_login_form,
    "get_auth_register_customer_form": get_auth_register_customer_form,
}
