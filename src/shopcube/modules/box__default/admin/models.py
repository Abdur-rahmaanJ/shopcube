"""
.. module:: AdminModels
   :synopsis: Contains model of a user Record

"""
import datetime
from sqlalchemy.ext.hybrid import hybrid_property
from flask_login import AnonymousUserMixin
from flask_login import UserMixin
from flask_login import login_manager
from itsdangerous import URLSafeTimedSerializer
from werkzeug.security import check_password_hash
from werkzeug.security import generate_password_hash

from init import db
from shopyo.api.models import PkModel

role_user_link = db.Table(
    "role_user_link",
    db.Column(
        "user_id",
        db.Integer,
        db.ForeignKey("users.id", ondelete="CASCADE"),
        primary_key=True,
    ),
    db.Column(
        "role_id",
        db.Integer,
        db.ForeignKey("roles.id", ondelete="CASCADE"),
        primary_key=True,
    ),
)


class AnonymousUser(AnonymousUserMixin):
    def set_password(self, password):
        return False

    def check_password(self, password):
        return False

    def avatar(self, size):
        return False

    @property
    def is_admin(self):
        return False

    # def get_reset_password_token(self, expires_in=current_app.config['FORGOT_PASSWORD_TOKEN_EXPIRE']):
    #     return False


login_manager.anonymous_user = AnonymousUser


class User(UserMixin, PkModel):
    """The user of the app"""

    __tablename__ = "users"

    username = db.Column(db.String(100), unique=True)
    _password = db.Column(db.String(128), nullable=False)
    first_name = db.Column(db.String(128))
    last_name = db.Column(db.String(128))
    is_admin = db.Column(db.Boolean, default=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    date_registered = db.Column(
        db.DateTime, nullable=False, default=datetime.datetime.now()
    )
    is_email_confirmed = db.Column(db.Boolean(), nullable=False, default=False)
    email_confirm_date = db.Column(db.DateTime)
    is_customer = db.Column(db.Boolean, default=False)

    # A user can have many roles and a role can have many users
    roles = db.relationship(
        "Role",
        secondary=role_user_link,
        backref="users",
    )

    @hybrid_property
    def password(self):
        return self._password

    @password.setter
    def password(self, plaintext):
        self._password = generate_password_hash(plaintext, method="sha256")

    def check_hash(self, password):
        return check_password_hash(self._password, password)

    def generate_confirmation_token(self, email):
        serializer = URLSafeTimedSerializer(app.config["SECRET_KEY"])
        return serializer.dumps(email, salt=app.config["PASSWORD_SALT"])

    @staticmethod
    def confirm_mail_token(self, token, expiration=3600):
        serializer = URLSafeTimedSerializer(app.config["SECRET_KEY"])
        try:
            email = serializer.loads(
                token, salt=app.config["PASSWORD_SALT"], max_age=expiration
            )
        except:
            return False
        return email

        def __repr__(self):
            return "User: {}".format(self.email)


class Role(PkModel):
    """A role for a user."""

    __tablename__ = "roles"
    name = db.Column(db.String(100), nullable=False)
