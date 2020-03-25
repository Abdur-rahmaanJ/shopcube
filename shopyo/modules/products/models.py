from addon import db


class Product(db.Model):
    __tablename__ = 'product'
    barcode = db.Column(db.String(100), primary_key=True)
    price = db.Column(db.Float)
    name = db.Column(db.String(100))
    description = db.Column(db.String(300))
    category = db.Column(db.String(50))
    date = db.Column(db.String(100))
    in_stock = db.Column(db.Integer)
    discontinued = db.Column(db.Boolean)
    selling_price = db.Column(db.Float)
    manufacturer_name = db.Column(db.String(100), db.ForeignKey('manufacturer.name'), nullable=False)
