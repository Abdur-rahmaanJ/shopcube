from datetime import datetime

from init import db
from shopyo.api.models import PkModel
from modules.box__ecommerce.product.models import Product

class Order(db.Model):
    __tablename__ = "orders"

    id = db.Column(db.Integer, primary_key=True)
    time = db.Column(db.DateTime, default=datetime.now())

    logged_in_customer_email = db.Column(db.String(120), default="")

    coupon = db.relationship(
        "Coupon", backref="coupon_order", lazy=True, uselist=False
    )

    order_items = db.relationship(
        "OrderItem",
        backref="item_order",
        lazy=True,
        cascade="all, delete, delete-orphan",
    )
    billing_detail = db.relationship(
        "BillingDetail",
        uselist=False,
        backref="billing_detail_order",
        cascade="all, delete, delete-orphan",
    )

    status = db.Column(
        db.String(120), default="pending"
    )  # pending, confirmed, shipped, cancelled, refunded

    payment_option_name = db.Column(db.String(120))
    payment_option_text = db.Column(db.String(120))

    shipment_option = db.relationship(
        "DeliveryOption",
        backref="shipment_option_order",
        lazy=True,
        uselist=False,
    )

    payment_option = db.relationship(
        "PaymentOption",
        backref="payment_option_order",
        lazy=True,
        uselist=False,
    )

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

    def get_std_formatted_time(self):
        return self.time.strftime("%b %d %Y, %H:%M")

    def get_ref(self):
        return '{}#{}'.format(int(self.id)*19, self.get_std_formatted_time())

    def get_total_amount(self):
        prices = []
        for item in self.order_items:
            product = item.get_product()
            price = product.selling_price * item.quantity
            prices.append(price)
        total_prices = sum(prices)
        return total_prices


class OrderItem(PkModel):
    __tablename__ = "order_items"


    time = db.Column(db.DateTime, default=datetime.now())
    quantity = db.Column(db.Integer)
    color = db.Column(db.String(100))
    size = db.Column(db.String(100))
    status = db.Column(
        db.String(120), default="pending"
    )
    barcode = db.Column(db.String(100), nullable=False)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'),
        nullable=False)

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

    def get_product(self):
        return Product.query.filter_by(barcode=self.barcode).first()


class BillingDetail(db.Model):
    __tablename__ = "billing_details"

    id = db.Column(db.Integer, primary_key=True)

    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))
    country = db.Column(db.String(100))
    street = db.Column(db.String(100))
    town_city = db.Column(db.String(100))
    phone = db.Column(db.String(100))
    email = db.Column(db.String(100))
    order_notes = db.Column(db.String(100))

    order_id = db.Column(db.Integer, db.ForeignKey("orders.id"))

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
