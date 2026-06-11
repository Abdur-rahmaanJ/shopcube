from datetime import datetime

from init import db


class Transaction(db.Model):
    __tablename__ = "transactions"

    id = db.Column(db.Integer, primary_key=True)

    cashier_id = db.Column(db.Integer)
    time = db.Column(db.DateTime, default=datetime.now)
    total_amount = db.Column(db.Numeric(10, 2), default=0.0)
    method_of_payment = db.Column(db.String(50))
    notes = db.Column(db.String(500))
    discount_type = db.Column(db.String(10))  # 'percentage' or 'fixed'
    discount_value = db.Column(db.Numeric(10, 2), default=0)

    items = db.relationship('TransactionItem', backref='transaction', lazy=True, cascade="all, delete-orphan")

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


class TransactionItem(db.Model):
    __tablename__ = "transaction_items"

    id = db.Column(db.Integer, primary_key=True)
    transaction_id = db.Column(db.Integer, db.ForeignKey('transactions.id'), nullable=False)
    product_barcode = db.Column(db.String(100), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    unit_price = db.Column(db.Numeric(10, 2), nullable=False)

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


class Shift(db.Model):
    __tablename__ = "shifts"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=True)
    opened_at = db.Column(db.DateTime, default=datetime.now)
    closed_at = db.Column(db.DateTime, nullable=True)
    starting_cash = db.Column(db.Numeric(10, 2), default=0)
    expected_cash = db.Column(db.Numeric(10, 2), default=0)
    actual_cash = db.Column(db.Numeric(10, 2), nullable=True)
    variance_cash = db.Column(db.Numeric(10, 2), nullable=True)
    notes = db.Column(db.Text)
    status = db.Column(db.String(20), default="open")

    def total_sales(self):
        q = Transaction.query.filter(Transaction.time >= self.opened_at)
        if self.closed_at:
            q = q.filter(Transaction.time <= self.closed_at)
        return sum(float(t.total_amount or 0) for t in q.all())

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()