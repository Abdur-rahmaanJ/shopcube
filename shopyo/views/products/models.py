from addon import db


class Product(db.Model):
    __tablename__ = 'product'
    barcode = db.Column(db.String(100), primary_key=True)
    price = db.Column(db.Float)
    name = db.Column(db.String(100))
    description = db.Column(db.String(300))
    category = db.Column(db.String(50))
    category_id = db.Column(db.Integer)
    stock = db.Column(db.Integer)
    supplier = db.Column(db.String(100))
    supplier_id = db.Column(db.Integer)
    discontinued = db.Column(db.Boolean)
    vat_price = db.Column(db.Float)
    selling_price = db.Column(db.Float)
    manufacturer = (db.Column(db.Integer(),
                    db.ForeignKey('manufacturer.id'), nullable=False))
