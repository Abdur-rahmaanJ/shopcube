"""
.. module:: AdminModels
   :synopsis: Contains model of a user Record

"""

from uuid import uuid4

from flask_login import AnonymousUserMixin
from flask_login import UserMixin
from flask_login import login_manager
from werkzeug.security import check_password_hash
from werkzeug.security import generate_password_hash

from shopyoapi.init import db

role_helpers = db.Table(
    "role_helpers",
    db.Column("user_id", db.Integer, db.ForeignKey("users.id")),
    db.Column("role_id", db.Integer, db.ForeignKey("roles.id")),
)


class AnonymousUser(AnonymousUserMixin):
    def set_password(self, password):
        return False

    def check_password(self, password):
        return False

    def avatar(self, size):
        return False

    def is_admin(self):
        return False

    # def get_reset_password_token(self, expires_in=current_app.config['FORGOT_PASSWORD_TOKEN_EXPIRE']):
    #     return False


login_manager.anonymous_user = AnonymousUser


class User(UserMixin, db.Model):
    """ User model """

    __tablename__ = "users"
    id = db.Column(db.String(10), primary_key=True)
    username = db.Column(db.String(100))
    password = db.Column(db.String(128))

    admin_user = db.Column(db.Boolean, default=False)
    roles = db.relationship("Role", secondary=role_helpers, cascade="all, delete")

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
        return f"User({self.username!r})"


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
