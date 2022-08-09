from datetime import datetime

from init import db


class Transaction(db.Model):
    __tablename__ = "transactions"

    id = db.Column(db.Integer, primary_key=True)

    chashier_id = db.Column(db.Integer)
    time = db.Column(db.DateTime, default=datetime.now())
    quantity = db.Column(db.Integer)
    price = db.Column(db.Float)

    def add(self):
        db.session.add(self)

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
