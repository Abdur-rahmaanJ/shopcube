from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)


class Products(db.Model):
    __tablename__ = 'products'
    barcode = db.Column(db.String(100), primary_key=True)
    price = db.Column(db.Float)
    vat_price = db.Column(db.Float)
    selling_price = db.Column(db.Float)
    manufacturer = db.Column(db.String(100), db.ForeignKey('manufacturers.name'))


class Manufacturers(db.Model):
    __tablename__ = 'manufacturers'
    name = db.Column(db.String(100), primary_key=True)

# db.DateTime, default=db.func.current_timestamp()
