from datetime import datetime

from init import db


class Transaction(db.Model):
    __tablename__ = "transactions"

    id = db.Column(db.Integer, primary_key=True)

    chashier_id = db.Column(db.Integer)
    time = db.Column(db.DateTime, default=datetime.now)
    quantity = db.Column(db.Integer)
    price = db.Column(db.Numeric(10, 2))
    total_amount = db.Column(db.Numeric(10, 2))
    method_of_payment = db.Column(db.String(50))

    product = db.relationship('Product', backref='transaction', lazy=True)

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
