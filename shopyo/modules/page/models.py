from shopyoapi.init import db
from datetime import datetime


class Page(db.Model):

    __tablename__ = "pages"
    id = db.Column(db.Integer, primary_key=True)
    created_date = db.Column(db.DateTime, default=datetime.now())
    title = db.Column(db.String(100))
    slug = db.Column(db.String(100))
    content = db.Column(db.String(1024))

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
