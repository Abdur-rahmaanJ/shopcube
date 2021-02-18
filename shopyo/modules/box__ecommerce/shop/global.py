from modules.box__ecommerce.shop.helpers import get_currency_symbol
from modules.box__ecommerce.shop.helpers import get_min_max_subcateg

from flask import session

def get_wishlist_data():
    if 'wishlist' not in session:
        session['wishlist'] = []
        return session['wishlist']

    return session['wishlist']

available_everywhere = {
    "get_currency_symbol": get_currency_symbol,
    'get_min_max_subcateg': get_min_max_subcateg,
    'get_wishlist_data': get_wishlist_data
}
