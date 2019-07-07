from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Products(db.Model):
    __tablename__ = 'products'
    barcode = db.Column(db.String(100), primary_key=True)
    price = db.Column(db.Float)
    vat_price = db.Column(db.Float)
    selling_price = db.Column(db.Float)
    manufacturer = db.Column(db.String(100), db.ForeignKey('manufacturers.name'))

class People(db.Model):
    __tablename__ = 'people'
    name = db.Column(db.String(100), primary_key=True)
    age = db.Column(db.Integer)
    birthday = db.Column(db.String(100))
    about = db.Column(db.String(100))
    social_media = db.Column(db.String(100))

class Manufacturers(db.Model):
    __tablename__ = 'manufacturers'
    name = db.Column(db.String(100), primary_key=True)

class Settings(db.Model):
    __tablename__ = 'settings'
    setting = db.Column(db.String(100), primary_key=True)
    value = db.Column(db.String(100))
# db.DateTime, default=db.func.current_timestamp()
