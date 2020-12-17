

from shopyoapi.init import db


class DeliveryOption(db.Model):

    __tablename__ = "deliveryoptions"
    id = db.Column(db.Integer, primary_key=True)
    option = db.Column(db.String(300))
    price = db.Column(db.Float)

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
