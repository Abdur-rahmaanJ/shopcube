"""
.. module:: AdminModels
   :synopsis: Contains model of a user Record

"""

from werkzeug.security import generate_password_hash, check_password_hash
from shopyoapi.init import db
from flask_login import UserMixin
from uuid import uuid4


class User(UserMixin, db.Model):
    """ User model """

    __tablename__ = "users"
    id = db.Column(db.String(10), primary_key=True)
    username = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(128))
    admin_user = db.Column(db.Boolean, default=False)

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        self.id = str(uuid4())

    def set_hash(self, password):
        self.password = generate_password_hash(password, method="sha256")

    def check_hash(self, password):
        return check_password_hash(self.password, password)

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def __repr__(self):
        return f'User({self.username!r})'
