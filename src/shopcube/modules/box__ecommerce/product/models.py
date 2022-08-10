from init import db
from shopyo.api.models import PkModel
from flask import url_for

# from modules.box__ecommerce.pos.models import Transaction

transaction_helpers = db.Table(
    "transaction_helpers",
    db.Column("product_barcode", db.Integer, db.ForeignKey("product.id")),
    db.Column("transaction_id", db.Integer, db.ForeignKey("transactions.id")),
)


class Product(PkModel):
    __tablename__ = "product"

    barcode = db.Column(db.String(100))
    price = db.Column(db.Float)
    name = db.Column(db.String(100))
    description = db.Column(db.String(300))
    date = db.Column(db.String(100))
    in_stock = db.Column(db.Integer)
    discontinued = db.Column(db.Boolean)
    selling_price = db.Column(db.Float)

    is_onsale = db.Column(db.Boolean, default=False)
    is_featured = db.Column(db.Boolean, default=False)
    subcategory_name = db.relationship("SubCategory", backref=db.backref("subcategory", uselist=False))
    transactions = db.relationship(
        "Transaction",
        secondary=transaction_helpers,
        backref="products",
        cascade="all, delete",
    )
    resources = db.relationship(
        "Resource", backref="resources", lazy=True, cascade="all, delete"
    )
    colors = db.relationship('Color', backref='color_product', lazy=True, cascade="all, delete, delete-orphan")
    sizes = db.relationship('Size', backref='size_product', lazy=True, cascade="all, delete, delete-orphan")

    # 
    subcategory_id = db.Column(db.Integer, db.ForeignKey('subcategories.id'),
        nullable=False)


    def get_color_string(self):
        return '\n'.join([c.name for c in self.colors])


    def get_size_string(self):
        return '\n'.join([s.name for s in self.sizes])

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

class Color(PkModel):

    __tablename__ = "color"


    name = db.Column(db.String(100))

    product_id = db.Column(db.Integer, db.ForeignKey('product.id'))


class Size(PkModel):

    __tablename__ = "size"


    name = db.Column(db.String(100))

    product_id = db.Column(db.Integer, db.ForeignKey('product.id'))