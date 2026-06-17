from shopyo_ecommerce.product.models import Product


def get_products():
    return Product.query.all()


available_everywhere = {
    "get_products": get_products,
}
