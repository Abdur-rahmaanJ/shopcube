from shopyoapi.init import db
from flask import url_for

# from modules.box__ecommerce.pos.models import Transaction

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

    is_onsale = db.Column(db.Boolean, default=False)
    is_featured = db.Column(db.Boolean, default=False)
    subcategory_name = db.Column(
        db.String(100), db.ForeignKey("subcategories.name")
    )
    transactions = db.relationship(
        "Transaction",
        secondary=transaction_helpers,
        backref="products",
        cascade="all, delete",
    )
    resources = db.relationship(
        "Resource", backref="resources", lazy=True, cascade="all, delete"
    )

    def get_one_image_url(self):
        if len(self.resources) == 0:
            return url_for('static', filename='default/default_product.jpg')
        else:
            resource = self.resources[0]
            return url_for('static', filename='uploads/products/{}'.format(resource.filename))

    def get_page_url(self):
        return url_for('shop.product', product_barcode=self.barcode)

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
