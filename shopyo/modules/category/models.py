"""
remember: backrefs should be unique
"""

from sqlalchemy import exists

from shopyoapi.init import db


class Category(db.Model):
    __tablename__ = "categories"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    subcategories = db.relationship("SubCategory", backref="category", lazy=True)
    resources = db.relationship(
        "Resource",
        backref="resource_category",
        lazy=True,
    )

    def insert(self):
        """Save category to the database"""
        db.session.add(self)
        db.session.commit()

    def update(self):
        """Update category"""
        db.session.commit()

    def delete(self):
        """delete category"""
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def category_exists(cls, name):
        return db.session.query(exists().where(cls.name == name)).scalar()


class SubCategory(db.Model):
    __tablename__ = "subcategories"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    category_name = db.Column(db.String(100), db.ForeignKey("categories.name"))
    # products = db.relationship(
    #     "Product", backref="subcategory", lazy=True, cascade="all, delete"
    # )
    products = db.relationship("Product", backref="subcategory", lazy=True)
    resources = db.relationship("Resource", backref="resource_subcategory", lazy=True)

    def insert(self):
        """Save category to the database"""
        db.session.add(self)
        db.session.commit()

    def update(self):
        """Update category"""
        db.session.commit()

    def delete(self):
        """delete category"""
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def category_exists(cls, name):
        return db.session.query(exists().where(cls.name == name)).scalar()
