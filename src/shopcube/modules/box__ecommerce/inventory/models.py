from shopyo.api.models import PkModel
from init import db


class InventoryCount(PkModel):
    __tablename__ = "inventory_counts"
    created_at = db.Column(db.DateTime, default=db.func.now())
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=True)
    notes = db.Column(db.Text)
    status = db.Column(db.String(20), default="draft")

    items = db.relationship("InventoryCountItem", backref="count", lazy=True, cascade="all, delete-orphan")

    def __repr__(self):
        return f"InventoryCount #{self.id} ({self.status})"


class InventoryCountItem(PkModel):
    __tablename__ = "inventory_count_items"
    count_id = db.Column(db.Integer, db.ForeignKey("inventory_counts.id"), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey("product.id"), nullable=False)
    expected_qty = db.Column(db.Integer, default=0)
    actual_qty = db.Column(db.Integer, default=0)

    product = db.relationship("Product", lazy=True)

    @property
    def variance(self):
        return (self.actual_qty or 0) - (self.expected_qty or 0)
