"""
.. module:: AdminModels
   :synopsis: Contains model of a user Record

"""

from werkzeug.security import generate_password_hash, check_password_hash
from shopyoapi.init import db
from flask_login import UserMixin
from uuid import uuid4


role_helpers = db.Table('role_helpers',
    db.Column('user_id', db.Integer, db.ForeignKey('users.id')),
    db.Column('role_id', db.Integer, db.ForeignKey('roles.id'))
)


class User(UserMixin, db.Model):
    """ User model """

    __tablename__ = "users"
    id = db.Column(db.String(10), primary_key=True)
    username = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(128))
    
    admin_user = db.Column(db.Boolean, default=False)
    roles = db.relationship("Role",
        secondary=role_helpers, 
        cascade = "all, delete")

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        self.id = str(uuid4())

    def set_hash(self, password):
        self.password = generate_password_hash(password, method="sha256")

    def check_hash(self, password):
        return check_password_hash(self.password, password)

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def __repr__(self):
        return f'User({self.username!r})'


class Role(db.Model):

    __tablename__ = "roles"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()


