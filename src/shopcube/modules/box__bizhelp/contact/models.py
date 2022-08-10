from datetime import datetime

from init import db


class ContactMessage(db.Model):

    __tablename__ = "contact"
    id = db.Column(db.Integer, primary_key=True)
    created_date = db.Column(db.DateTime, default=datetime.now())
    name = db.Column(db.String(100))
    email = db.Column(db.String(100))
    message = db.Column(db.String(1024))

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
