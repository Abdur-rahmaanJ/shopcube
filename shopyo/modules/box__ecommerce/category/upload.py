import datetime
import uuid

from app import app

from modules.box__ecommerce.category.models import Category
from modules.box__ecommerce.category.models import SubCategory
from modules.box__ecommerce.product.models import Product


def add_uncategorised_category():
    with app.app_context():
        category = Category(name="uncategorised")
        subcategory = SubCategory(name="uncategorised")
        p1 = Product(
            barcode=str(uuid.uuid1()),
            price=10.0,
            name="Apple",
            in_stock=50,
            selling_price=15.0,
            discontinued=False,
            description="",
        )
        p2 = Product(
            barcode=str(uuid.uuid1()),
            price=10.0,
            name="Pear",
            in_stock=50,
            selling_price=15.0,
            discontinued=False,
            description="",
        )
        p3 = Product(
            barcode=str(uuid.uuid1()),
            price=10.0,
            name="Peach",
            in_stock=50,
            selling_price=15.0,
            discontinued=False,
            description="",
        )

        subcategory.products.extend([p1, p2, p3])
        category.subcategories.append(subcategory)
        category.save()

def add_food_category():
    with app.app_context():
        category = Category(name="Food")
        subcategory = SubCategory(name="Fruit")
        p1 = Product(
            barcode=str(uuid.uuid1()),
            price=10.0,
            name="Apple",
            in_stock=50,
            selling_price=15.0,
            discontinued=False,
            description="",
        )
        p2 = Product(
            barcode=str(uuid.uuid1()),
            price=10.0,
            name="Pear",
            in_stock=50,
            selling_price=15.0,
            discontinued=False,
            description="",
        )
        p3 = Product(
            barcode=str(uuid.uuid1()),
            price=10.0,
            name="Peach",
            in_stock=50,
            selling_price=15.0,
            discontinued=False,
            description="",
        )

        subcategory.products.extend([p1, p2, p3])
        category.subcategories.append(subcategory)
        category.save()

def upload():
    # print("Adding category and subcategory uncategorised ...")
    # add_uncategorised_category()
    print('Add food category')
    add_food_category()
