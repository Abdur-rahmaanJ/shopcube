from init import db


class DeliveryOption(db.Model):

    __tablename__ = "deliveryoptions"
    id = db.Column(db.Integer, primary_key=True)
    option = db.Column(db.String(300))
    price = db.Column(db.Float)

    order_id = db.Column(db.Integer, db.ForeignKey("orders.id"))

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()


class PaymentOption(db.Model):

    __tablename__ = "paymentoptions"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(300))
    text = db.Column(db.String(300))

    order_id = db.Column(db.Integer, db.ForeignKey("orders.id"))

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()


class Coupon(db.Model):

    __tablename__ = "coupons"
    id = db.Column(db.Integer, primary_key=True)
    string = db.Column(db.String(300))
    type = db.Column(db.String(300))  # percentage, value
    value = db.Column(db.String(300))

    order_id = db.Column(db.Integer, db.ForeignKey("orders.id"))

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
