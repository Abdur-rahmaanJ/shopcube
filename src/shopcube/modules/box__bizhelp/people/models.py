from init import db


class People(db.Model):
    __tablename__ = "people"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    phone = db.Column(db.Integer)
    mobile = db.Column(db.Integer)
    email = db.Column(db.String(100))
    facebook = db.Column(db.String(128))
    twitter = db.Column(db.String(128))
    linkedin = db.Column(db.String(128))
    age = db.Column(db.Integer)
    birthday = db.Column(db.String(100))
    notes = db.Column(db.String(100))
    is_manufacturer = db.Column(db.Boolean)
    manufacturer_name = db.Column(db.String(100))
    manufacturer_phone = db.Column(db.Integer)
    manufacturer_address = db.Column(db.String(200))
