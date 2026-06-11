from shopyo.api.models import PkModel
from init import db


class Location(PkModel):
    __tablename__ = "locations"
    name = db.Column(db.String(200), nullable=False)
    address = db.Column(db.Text)
    is_active = db.Column(db.Boolean, default=True)

    def __repr__(self):
        return f"Location: {self.name}"


class StockPerLocation(PkModel):
    __tablename__ = "stock_per_location"
    product_id = db.Column(db.Integer, db.ForeignKey("product.id"), nullable=False)
    location_id = db.Column(db.Integer, db.ForeignKey("locations.id"), nullable=False)
    quantity = db.Column(db.Integer, default=0)

    product = db.relationship("Product", lazy=True)
    location = db.relationship("Location", lazy=True)


class StockTransfer(PkModel):
    __tablename__ = "stock_transfers"
    from_location_id = db.Column(db.Integer, db.ForeignKey("locations.id"), nullable=False)
    to_location_id = db.Column(db.Integer, db.ForeignKey("locations.id"), nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.now())
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=True)
    status = db.Column(db.String(20), default="draft")
    notes = db.Column(db.Text)

    from_location = db.relationship("Location", foreign_keys=[from_location_id], lazy=True)
    to_location = db.relationship("Location", foreign_keys=[to_location_id], lazy=True)
    items = db.relationship("StockTransferItem", backref="transfer", lazy=True, cascade="all, delete-orphan")


class StockTransferItem(PkModel):
    __tablename__ = "stock_transfer_items"
    transfer_id = db.Column(db.Integer, db.ForeignKey("stock_transfers.id"), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey("product.id"), nullable=False)
    quantity = db.Column(db.Integer, default=0)

    product = db.relationship("Product", lazy=True)


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
