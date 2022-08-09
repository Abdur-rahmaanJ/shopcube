"""
remember: backrefs should be unique
"""

from sqlalchemy import exists
from sqlalchemy.orm import validates

from init import db
from shopyo.api.models import PkModel
from flask import url_for


class Category(PkModel):
    __tablename__ = "categories"
    name = db.Column(db.String(100), unique=True, nullable=False)
    subcategories = db.relationship(
        "SubCategory", backref="category", lazy=True
    )
    resources = db.relationship(
        "Resource",
        backref="resource_category",
        lazy=True,
    )

    def __repr__(self):
        return f"Category: {self.name}"

    @classmethod
    def category_exists(cls, name):
        return db.session.query(
            exists().where(cls.name == name.lower())
        ).scalar()

    @validates("name")
    def convert_lower(self, key, value):
        return value.lower()

    def get_one_image_url(self):
        if len(self.resources) == 0:
            return url_for('static', filename='default/default_subcategory.jpg')
        else:
            resource = self.resources[0]
            return url_for('static', filename='uploads/products/{}'.format(resource.filename))

    def get_page_url(self):
        return url_for('shop.category', category_name=self.name)


class SubCategory(PkModel):
    __tablename__ = "subcategories"
    name = db.Column(db.String(100), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey("categories.id"))
    products = db.relationship("Product", backref="subcategory", lazy=True)
    resources = db.relationship(
        "Resource", backref="resource_subcategory", lazy=True
    )

    @classmethod
    def category_exists(cls, name):
        return db.session.query(
            exists().where(cls.name == name.lower())
        ).scalar()

    @validates("name")
    def convert_lower(self, key, value):
        return value.lower()

    def get_num_products(self):
        return len(self.products)

    def get_one_image_url(self):

        if len(self.products) > 0:
            product = self.products[0]
            if len(product.resources) == 0:
                if len(self.resources) == 0:
                    return url_for('static', filename='default/default_subcategory.jpg')
                else:
                    resource = self.resources[0]
                    return url_for('static', filename='uploads/subcategory/{}'.format(resource.filename))
            else:
                resource = product.resources[0]
                return url_for('static', filename='uploads/products/{}'.format(resource.filename))
        else:
            if len(self.resources) == 0:
                return url_for('static', filename='default/default_subcategory.jpg')
            else:
                resource = self.resources[0]
                return url_for('static', filename='uploads/subcategory/{}'.format(resource.filename))
