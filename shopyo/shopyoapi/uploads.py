from werkzeug.security import generate_password_hash

from app import app

from shopyoapi.init import db

from modules.admin.models import Role
from modules.admin.models import User
from modules.category.models import Category
from modules.category.models import SubCategory
from modules.settings.models import Settings

import datetime


def add_admin(email, password):
    with app.app_context():
        user = User()
        user.email = email
        user.password = generate_password_hash(password, method="sha256")
        user.is_admin = True
        user.email_confirmed = True
        email_confirm_date = datetime.datetime.now()
        user.insert()


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
        category.subcategories.append(SubCategory(name="uncategorised"))
        category.insert()
