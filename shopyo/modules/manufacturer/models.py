from addon import db
from sqlalchemy import exists


class Manufacturer(db.Model):
    __tablename__ = 'manufacturer'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    products = db.relationship(
        'Product', backref='manufacturers', lazy=True, cascade="all, delete")

    def insert(self):
        """Save manufacturer to the database"""
        db.session.add(self)
        db.session.commit()

    def update(self):
        """Update manufacturer"""
        db.session.commit()

    def delete(self):
        """delete manufacturer"""
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def manufacturer_exists(cls, name):
        return db.session.query(exists().where(cls.name == name)).scalar()
