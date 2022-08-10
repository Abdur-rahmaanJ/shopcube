from init import db


class Appointments(db.Model):
    __tablename__ = "appointments"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    date = db.Column(db.String(20))
    time = db.Column(db.String(20))
    active = db.Column(db.String(20))
