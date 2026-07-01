from shopyo.api.models import PkModel
from init import db


class Vendor(PkModel):
    __tablename__ = "shopyo_ecommerce_vendors"
    name = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(120))
    phone = db.Column(db.String(50))
    address = db.Column(db.Text)
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=db.func.now())

    products = db.relationship("Product", backref="vendor", lazy=True)

    def __repr__(self):
        return f"Vendor: {self.name}"

    def insert(self):
        db.session.add(self)
        db.session.commit()
        return self
