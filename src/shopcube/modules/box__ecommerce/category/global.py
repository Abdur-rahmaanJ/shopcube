from modules.box__ecommerce.category.models import Category


def get_categories():
    return Category.query.all()


available_everywhere = {
    "get_categories": get_categories,
    "Category": Category
}
