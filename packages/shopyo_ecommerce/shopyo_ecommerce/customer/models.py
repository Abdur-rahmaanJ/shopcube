from shopyo.api.models import PkModel
from init import db


class CustomerGroup(PkModel):
    __tablename__ = "shopyo_ecommerce_customer_groups"
    name = db.Column(db.String(100), unique=True, nullable=False)
    discount_percent = db.Column(db.Numeric(5, 2), default=0)


class Customer(db.Model):
    __tablename__ = "shopyo_ecommerce_customer"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120))
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))
    phone = db.Column(db.String(50))
    total_spent = db.Column(db.Numeric(10, 2), default=0)
    order_count = db.Column(db.Integer, default=0)
    last_purchase = db.Column(db.DateTime, nullable=True)
    group_id = db.Column(db.Integer, db.ForeignKey("shopyo_ecommerce_customer_groups.id"), nullable=True)
    group = db.relationship("CustomerGroup", backref="customers", lazy=True)

    def avg_order_value(self):
        return float(self.total_spent or 0) / max(self.order_count or 1, 1)

    def insert(self):
        db.session.add(self)
        db.session.commit()
        return self

    def update(self):
        db.session.commit()
