"""Factories to help in tests."""
from factory import Sequence
from factory.alchemy import SQLAlchemyModelFactory

from init import db
from modules.box__default.auth.models import User
from modules.box__default.auth.models import Role
from sqlalchemy.orm import scoped_session


class BaseFactory(SQLAlchemyModelFactory):
    """Base factory."""

    class Meta:
        """Factory configuration."""

        abstract = True
        sqlalchemy_session = db.session
        sqlalchemy_session = scoped_session(
            lambda: db.session, scopefunc=lambda: db.session
        )
        sqlalchemy_session_persistence = "commit"


class UserFactory(BaseFactory):
    """User factory."""

    username = Sequence(lambda n: f"user{n}")
    email = Sequence(lambda n: f"user{n}@example.com")
    password = "pass"
    is_email_confirmed = True
    is_admin = False

    class Meta:
        """Factory configuration."""

        model = User


class RoleFactory(BaseFactory):
    """Role factory."""

    name = Sequence(lambda n: f"role{n}")

    class Meta:
        """Factory configuration."""

        model = Role
