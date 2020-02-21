from werkzeug.security import generate_password_hash, check_password_hash
from addon import db
from flask_login import UserMixin



class Users(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.String(10), primary_key=True)
    name = db.Column(db.String(100))
    password = db.Column(db.String(128))
    admin_user = db.Column(db.Boolean, default=False)

    def set_hash(self, password):
        self.password = generate_password_hash(password, method="sha256")

    def check_hash(self, password):
        return check_password_hash(self.password, password)


class Products(db.Model):
    __tablename__ = 'products'
    barcode = db.Column(db.String(100), primary_key=True)
    price = db.Column(db.Float)#

    vat_price = db.Column(db.Float)
    selling_price = db.Column(db.Float)
    manufacturer = (db.Column(db.String(100),
                    db.ForeignKey('manufacturers.name')))


class People(db.Model):
    __tablename__ = 'people'
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



class Manufacturers(db.Model):
    __tablename__ = 'manufacturers'
    name = db.Column(db.String(100), primary_key=True)


class Appointments(db.Model):
    __tablename__ = 'appointments'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    date = db.Column(db.String(20))
    time = db.Column(db.String(20))
    active = db.Column(db.String(20))


class Settings(db.Model):
    __tablename__ = 'settings'
    setting = db.Column(db.String(100), primary_key=True)
    value = db.Column(db.String(100))


class Patients(db.Model):
    __tablename__ = 'patients'
    first_name = db.Column(db.String(100), primary_key=True)
    last_name = db.Column(db.String(100))

