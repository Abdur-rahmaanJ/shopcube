from shopyoapi.init import db
from modules.pos.models import Transaction

transaction_helpers = db.Table(
    "transaction_helpers",
    db.Column("product_barcode", db.Integer, db.ForeignKey("product.barcode")),
    db.Column("transaction_id", db.Integer, db.ForeignKey("transactions.id")),
)
class Product(db.Model):
    __tablename__ = "product"
    barcode = db.Column(db.String(100), primary_key=True)
    price = db.Column(db.Float)
    name = db.Column(db.String(100))
    description = db.Column(db.String(300))
    date = db.Column(db.String(100))
    in_stock = db.Column(db.Integer)
    discontinued = db.Column(db.Boolean)
    selling_price = db.Column(db.Float)
    category_name = db.Column(
        db.String(100), db.ForeignKey("category.name"), nullable=False
    )
    transactions = db.relationship("Transaction", secondary=transaction_helpers, backref="products", cascade="all, delete")

    def add(self):
        """Save category to the database"""
        db.session.add(self)

    def insert(self):
        """Save category to the database"""
        db.session.add(self)
        db.session.commit()

    def update(self):
        """Update category"""
        db.session.commit()

    def delete(self):
        """delete category"""
        db.session.delete(self)
        db.session.commit()

