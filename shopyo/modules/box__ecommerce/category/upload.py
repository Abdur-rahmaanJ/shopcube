import datetime
import uuid

from app import app

from modules.box__ecommerce.category.models import Category
from modules.box__ecommerce.category.models import SubCategory
from modules.box__ecommerce.product.models import Product
from modules.box__ecommerce.product.models import Color
from modules.box__ecommerce.product.models import Size


colors = [Color(name='c1')]
sizes = [Size(name='s1')]
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
        p1.colors = colors
        p1.sizes = sizes

        p2 = Product(
            barcode=str(uuid.uuid1()),
            price=10.0,
            name="Pear",
            in_stock=50,
            selling_price=15.0,
            discontinued=False,
            description="",
        )
        p2.colors = colors
        p2.sizes = sizes

        p3 = Product(
            barcode=str(uuid.uuid1()),
            price=10.0,
            name="Peach",
            in_stock=50,
            selling_price=15.0,
            discontinued=False,
            description="",
        )
        p3.colors = colors
        p3.sizes = sizes


        subcategory.products.extend([p1, p2, p3])
        category.subcategories.append(subcategory)
        category.save()

def add_men_category():
    with app.app_context():
        category = Category(name="Men")
        subcategory1 = SubCategory(name="Sneakers")
        subcategory2 = SubCategory(name="Air Jordan")
        subcategory3 = SubCategory(name="Slides")
        subcategory4 = SubCategory(name="Airmax")
        p1 = Product(
            barcode=str(uuid.uuid1()),
            price=10.0,
            name="Demo Shoe 1",
            in_stock=50,
            selling_price=15.0,
            discontinued=False,
            description="",
        )
        p1.sizes = sizes
        p1.colors = colors

        p2 = Product(
            barcode=str(uuid.uuid1()),
            price=10.0,
            name="Demo Shoe 2",
            in_stock=50,
            selling_price=15.0,
            discontinued=False,
            description="",
        )
        p2.sizes = sizes
        p2.colors = colors

        p3 = Product(
            barcode=str(uuid.uuid1()),
            price=10.0,
            name="Demo Shoe 3",
            in_stock=50,
            selling_price=15.0,
            discontinued=False,
            description="",
        )
        p3.sizes = sizes
        p3.colors = colors

        p4 = Product(
            barcode=str(uuid.uuid1()),
            price=10.0,
            name="Demo Shoe 4",
            in_stock=50,
            selling_price=15.0,
            discontinued=False,
            description="",
        )
        p4.sizes = sizes
        p4.colors = colors


        subcategory2.save(commit=False)
        subcategory3.save(commit=False)
        subcategory4.save(commit=False)


        subcategory1.products.extend([p1, p2, p3, p4])
        category.subcategories.extend([
            subcategory1,
            subcategory2,
            subcategory3,
            subcategory4
            ])
        category.save()

def add_women_category():
    with app.app_context():
        category = Category(name="Women")
        subcategory1 = SubCategory(name="Sneakers")
        subcategory2 = SubCategory(name="Air Jordan")
        subcategory3 = SubCategory(name="Slides")
        subcategory4 = SubCategory(name="Airmax")

        subcategory2.save(commit=False)
        subcategory3.save(commit=False)
        subcategory4.save(commit=False)
        subcategory1.save(commit=False)

        category.subcategories.extend([
            subcategory1,
            subcategory2,
            subcategory3,
            subcategory4
            ])
        category.save()

def upload():
    # print("Adding category and subcategory uncategorised ...")
    # add_uncategorised_category()
    print('Add category')
    add_men_category()
    add_women_category()
