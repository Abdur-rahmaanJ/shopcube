from werkzeug.security import generate_password_hash, check_password_hash
from addon import db
from flask_login import UserMixin
from sqlalchemy import exists


class Users(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.String(10), primary_key=True)
    name = db.Column(db.String(100))
    password = db.Column(db.String(128))
    admin_user = db.Column(db.Boolean, default=False)

    def set_hash(self, password):
        self.password = generate_password_hash(password, method="sha256")

    def check_hash(self, password):
        return check_password_hash(self.password, password)
