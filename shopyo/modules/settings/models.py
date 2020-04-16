from shopyoapi.init import db


class Settings(db.Model):
    __tablename__ = "settings"
    setting = db.Column(db.String(100), primary_key=True)
    value = db.Column(db.String(100))
