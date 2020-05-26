from shopyoapi.init import db
from sqlalchemy import exists


class Category(db.Model):
    __tablename__ = "category"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    products = db.relationship(
        "Product", backref="categories", lazy=True, cascade="all, delete"
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
