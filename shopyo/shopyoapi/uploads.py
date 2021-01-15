import datetime
import uuid

from werkzeug.security import generate_password_hash

from app import app
from shopyoapi.init import db
from modules.box__default.admin.models import User
from modules.box__ecommerce.category.models import Category
from modules.box__ecommerce.category.models import SubCategory
from modules.box__ecommerce.product.models import Product
from modules.box__default.settings.models import Settings


def add_admin(email, password):
    with app.app_context():
        user = User()
        user.email = email
        user.password = generate_password_hash(password, method="sha256")
        user.is_admin = True
        user.email_confirmed = True
        user.email_confirm_date = datetime.datetime.now()
        user.save()


def add_setting(name, value):
    with app.app_context():
        if Settings.query.filter_by(setting=name).first():
            s = Settings.query.get(name)
            s.value = value
            db.session.commit()
        else:
            s = Settings(setting=name, value=value)
            db.session.add(s)
            db.session.commit()


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
        category.insert()
