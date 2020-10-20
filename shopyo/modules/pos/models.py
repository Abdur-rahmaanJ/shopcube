from shopyoapi.init import db
from flask_login import current_user

class Transaction(db.Model):
    __tablename__ = "transactions"

    id = db.Column(db.Integer, primary_key=True)
    chashier_id = db.Column(db.Integer, default=current_user.id)
    products = db.relationship(
        "Product", backref="transaction", lazy=True, cascade="all, delete"
    )
