from shopyo.api.models import PkModel
from init import db


class PurchaseOrder(PkModel):
    __tablename__ = "purchase_orders"
    vendor_id = db.Column(db.Integer, db.ForeignKey("vendors.id"), nullable=True)
    status = db.Column(db.String(20), default="draft")
    created_at = db.Column(db.DateTime, default=db.func.now())
    updated_at = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now())
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=True)
    notes = db.Column(db.Text)

    vendor = db.relationship("Vendor", backref="purchase_orders", lazy=True)
    items = db.relationship("PurchaseOrderItem", backref="order", lazy=True, cascade="all, delete-orphan")

    def total_cost(self):
        return sum(item.subtotal() for item in self.items)

    def __repr__(self):
        return f"PO #{self.id} ({self.status})"


class PurchaseOrderItem(PkModel):
    __tablename__ = "purchase_order_items"
    purchase_order_id = db.Column(db.Integer, db.ForeignKey("purchase_orders.id"), nullable=False)
    product_barcode = db.Column(db.String(100))
    product_name = db.Column(db.String(200))
    quantity_ordered = db.Column(db.Integer, default=1)
    quantity_received = db.Column(db.Integer, default=0)
    unit_price = db.Column(db.Numeric(10, 2), default=0)

    def subtotal(self):
        return (self.quantity_received or 0) * float(self.unit_price or 0)

    def __repr__(self):
        return f"POItem({self.product_name} x{self.quantity_ordered})"
