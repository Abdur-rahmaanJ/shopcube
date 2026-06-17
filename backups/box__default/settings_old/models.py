from init import db


class Settings(db.Model):
    __tablename__ = "settings"
    setting = db.Column(db.String(100), primary_key=True)
    value = db.Column(db.String(100))

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
