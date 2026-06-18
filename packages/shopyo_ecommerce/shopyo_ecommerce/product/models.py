from datetime import datetime

from flask import url_for
from flask_login import current_user

from shopyo.api.models import PkModel

from init import db

# from shopyo_ecommerce.pos.models import Transaction




class Product(PkModel):
    __tablename__ = "shopyo_ecommerce_product"

    barcode = db.Column(db.String(100))
    price = db.Column(db.Numeric(10, 2))
    name = db.Column(db.String(100))
    description = db.Column(db.String(300))
    date = db.Column(db.String(100))
    in_stock = db.Column(db.Integer)
    min_stock = db.Column(db.Integer, default=0)
    cost_price = db.Column(db.Numeric(10, 2), default=0)
    discontinued = db.Column(db.Boolean)
    selling_price = db.Column(db.Numeric(10, 2))
    is_onsale = db.Column(db.Boolean, default=False)
    is_featured = db.Column(db.Boolean, default=False)
    is_variable_qty = db.Column(db.Boolean, default=False)
    unit_label = db.Column(db.String(20), default="ml")
    unit_step = db.Column(db.Numeric(10, 2), default=1.0)

    resources = db.relationship(
        "Resource", backref="resources", lazy=True, cascade="all, delete"
    )
    colors = db.relationship(
        "Color",
        backref="color_product",
        lazy=True,
        cascade="all, delete, delete-orphan",
    )
    sizes = db.relationship(
        "Size",
        backref="size_product",
        lazy=True,
        cascade="all, delete, delete-orphan",
    )

    vendor_id = db.Column(db.Integer, db.ForeignKey("shopyo_ecommerce_vendors.id"), nullable=True)

    subcategory_id = db.Column(
        db.Integer, db.ForeignKey("shopyo_ecommerce_subcategories.id"), nullable=False
    )

    bundle_components = db.relationship(
        "BundleComponent",
        foreign_keys="BundleComponent.bundle_product_id",
        backref="bundle_product",
        lazy=True,
        cascade="all, delete-orphan",
    )

    def stock_at(self, location_id):
        from shopyo_ecommerce.inventory.models import StockPerLocation
        spl = StockPerLocation.query.filter_by(product_id=self.id, location_id=location_id).first()
        return spl.quantity if spl else 0

    def set_stock(self, location_id, quantity):
        from shopyo_ecommerce.inventory.models import StockPerLocation
        spl = StockPerLocation.query.filter_by(product_id=self.id, location_id=location_id).first()
        if spl:
            spl.quantity = quantity
        else:
            spl = StockPerLocation(product_id=self.id, location_id=location_id, quantity=quantity)
            db.session.add(spl)
        db.session.commit()

    def get_color_string(self):
        return "\n".join([c.name for c in self.colors])

    def get_size_string(self):
        return "\n".join([f"{s.name}:{s.price}" if s.price else s.name for s in self.sizes])

    def get_one_image_url(self):
        if len(self.resources) == 0:
            return url_for("static", filename="default/default_product.jpg")
        else:
            resource = self.resources[0]
            return url_for(
                "static", filename=f"uploads/products/{resource.filename}"
            )

    def get_page_url(self):
        return url_for("shopyo_ecommerce.shop.product", product_barcode=self.barcode)

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


    def log_adjustment(self, quantity_change, reason, reference=""):
        adj = StockAdjustment(
            product_id=self.id,
            quantity_change=quantity_change,
            reason=reason,
            reference=reference,
            user_id=current_user.id if current_user.is_authenticated else None,
        )
        adj.save()


class StockAdjustment(PkModel):
    __tablename__ = "shopyo_ecommerce_stock_adjustments"
    product_id = db.Column(db.Integer, db.ForeignKey("shopyo_ecommerce_product.id"), nullable=False)
    quantity_change = db.Column(db.Integer, nullable=False)
    reason = db.Column(db.String(200), nullable=False)
    reference = db.Column(db.String(200), default="")
    created_at = db.Column(db.DateTime, default=db.func.now())
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=True)

    product = db.relationship("Product", backref="stock_adjustments", lazy=True)

    def __repr__(self):
        return f"StockAdjustment(product={self.product_id}, change={self.quantity_change})"


class Color(PkModel):

    __tablename__ = "shopyo_ecommerce_color"

    name = db.Column(db.String(100))

    product_id = db.Column(db.Integer, db.ForeignKey("shopyo_ecommerce_product.id"))


class BundleComponent(PkModel):
    __tablename__ = "shopyo_ecommerce_bundle_components"
    bundle_product_id = db.Column(db.Integer, db.ForeignKey("shopyo_ecommerce_product.id"), nullable=False)
    component_product_id = db.Column(db.Integer, db.ForeignKey("shopyo_ecommerce_product.id"), nullable=False)
    quantity = db.Column(db.Integer, default=1)

    component = db.relationship("Product", foreign_keys=[component_product_id], lazy=True)


class Size(PkModel):
    __tablename__ = "shopyo_ecommerce_size"
    name = db.Column(db.String(100))
    product_id = db.Column(db.Integer, db.ForeignKey("shopyo_ecommerce_product.id"))
    price = db.Column(db.Numeric(10, 2), nullable=True)
