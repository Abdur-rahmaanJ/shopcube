"""
This file (test_auth_models.py) contains the units tests for
the all `auth` module's models.
"""
import pytest
import datetime as dt
from freezegun import freeze_time
from modules.box__default.auth.models import User
from modules.box__default.auth.models import Role
from modules.box__default.auth.models import AnonymousUser
from modules.box__default.auth.models import role_user_bridge
from modules.box__default.auth.tests.factories import UserFactory
from modules.box__default.auth.tests.factories import RoleFactory
from sqlalchemy.exc import IntegrityError


class TestAuthFactory:
    """ Test all Model Factories in Auth """

    def test_user_factory(self):
        user = UserFactory()
        retrived = user.query.get(user.id)

        assert retrived is not None
        assert bool(retrived.username)
        assert bool(retrived.email)
        assert bool(retrived.password)
        assert retrived.is_email_confirmed is True
        assert retrived.is_admin is False
        assert retrived.check_password("pass")

    def test_role_factory(self):
        role = RoleFactory()
        retrived = Role.query.get(role.id)

        assert retrived is not None
        assert bool(retrived.name)


class TestAnonymousUser:
    """ tests app's anonymous users characteristics """

    def test_anonymous_user_is_admin(self):
        user = AnonymousUser()

        assert user.is_admin is False

    @pytest.mark.parametrize(
        "email_config",
        [
            ("EMAIL_CONFIRMATION_DISABLED", "remove"),
            ("EMAIL_CONFIRMATION_DISABLED", False),
            ("EMAIL_CONFIRMATION_DISABLED", None),
            ("EMAIL_CONFIRMATION_DISABLED", "random string"),
        ],
        indirect=True,
    )
    def test_anonymous_user_email_confirmed_disabled(self, email_config):
        user = AnonymousUser()

        assert user.is_email_confirmed is False

    @pytest.mark.parametrize(
        "email_config",
        [
            ("EMAIL_CONFIRMATION_DISABLED", True),
        ],
        indirect=True,
    )
    def test_anonymous_user_has_email_confirmed_enabled(self, email_config):
        user = AnonymousUser()

        assert user.is_email_confirmed is True

    def test_anonymous_username_is_set(self):
        user = AnonymousUser()

        assert bool(user.username)

    def test_anonymous_email_is_set(self):
        user = AnonymousUser()

        assert bool(user.email)

    def test_anonymous_user_representation(self):

        user = AnonymousUser()

        assert repr(user) == "<AnonymousUser guest>"


class TestUser:
    """ Test User model """

    def test_get_user_by_id(self):
        user = User.create(email="foo@bar.com", password="pass")
        retrieved = User.get_by_id(user.id)

        assert retrieved == user

    def test_email_is_unique(self):
        User.create(email="foo@bar.com", password="pass")

        with pytest.raises(IntegrityError):
            User.create(email="foo@bar.com", password="another")

    def test_username_is_unique(self):
        User.create(username="foo", email="foo@bar.com", password="pass")

        with pytest.raises(IntegrityError):
            User.create(username="foo", email="bar@bar.com", password="pass")

    def test_email_is_not_nullable(self):
        with pytest.raises(IntegrityError):
            User.create(username="foo", password="pass")

    def test_password_is_not_nullable(self):
        with pytest.raises(IntegrityError):
            User.create(username="foo")

    def test_user_is_not_admin_by_default(self):
        user = User.create(email="foo@bar.com", password="pass")

        assert user.is_admin is False

    def test_date_registered_at_defaults_to_datetime(self):
        user = User.create(email="foo@bar.com", password="pass")

        assert bool(user.date_registered)
        assert isinstance(user.date_registered, dt.datetime)

    def test_email_is_not_confirmed_by_default(self):
        user = User.create(email="foo@bar.com", password="pass")

        assert user.is_email_confirmed is False

    def test_check_password(self):
        user = User.create(email="foo@bar.com", password="foobar123$")

        assert user.check_password("foobaz123") is False
        assert user.check_password("foobar123$")

    def test_password_hashed_on_user_creation(self):
        user = User.create(email="foo@bar.com", password="foobar123$")

        assert user.password != "foobar123$"

    def test_user_representation(self):
        user = User.create(email="foo@bar.com", password="foobar123$")

        assert repr(user) == f"<User-id: {user.id}, User-email: foo@bar.com>"

    def test_valid_token_confirms_email(self):
        user = User()
        user.email = "foo@bar.com"
        user.password = "pass"
        user.is_email_confirmed = False
        user.save()
        token = user.generate_confirmation_token()
        confirm_status = user.confirm_token(token)

        assert confirm_status is True
        assert user.is_email_confirmed

    @freeze_time("Jan 14th, 2020", auto_tick_seconds=200)
    def test_expired_token_does_not_confirm_email(self):
        user = User.create(email="foo@bar.com", password="foobar123$")
        token = user.generate_confirmation_token()
        confirm_status = user.confirm_token(token, expiration=120)

        assert confirm_status is False
        assert not user.is_email_confirmed

    def test_email_should_only_be_confirmed_from_same_email(self):
        user1 = UserFactory(is_email_confirmed=False)
        user2 = UserFactory(is_email_confirmed=False)
        token = user1.generate_confirmation_token()
        confirm_status = user2.confirm_token(token)

        assert confirm_status is False
        assert not user2.is_email_confirmed
        assert not user1.is_email_confirmed


class TestRole:
    """ Test Role model """

    def test_get_role_by_id(self):
        role = Role.create(name="buyer")
        retrieved = Role.get_by_id(role.id)

        assert retrieved == role

    def test_role_representation(self):
        role = Role.create(name="buyer")

        assert repr(role) == f"<Role-id: {role.id}, Role-name: buyer>"


class TestUserRoleRelation:
    """ Test User and Role model relationship """

    def test_user_can_have_many_roles(self):
        user = UserFactory()
        roles = RoleFactory.create_batch(2)
        user.roles = roles
        user.save()
        retrived_role1 = Role.query.get(roles[0].id)
        retrived_role2 = Role.query.get(roles[1].id)

        assert retrived_role1 is not None
        assert retrived_role2 is not None
        assert retrived_role1.users[0] == user
        assert retrived_role2.users[0] == user

    def test_role_can_have_many_users(self):
        role = RoleFactory()
        users = UserFactory.create_batch(2)
        role.users = users
        role.save()
        retrived_user1 = User.query.get(users[0].id)
        retrived_user2 = User.query.get(users[1].id)

        assert retrived_user1 is not None
        assert retrived_user2 is not None
        assert retrived_user1.roles[0] == role
        assert retrived_user2.roles[0] == role

    def test_deleting_role_does_not_remove_user(self):
        user = UserFactory()
        roles = RoleFactory.create_batch(3)
        user.roles = roles
        user.save()
        roles[0].delete()
        retrived_roles = Role.query.all()
        retrived_user = User.get_by_id(user.id)

        assert retrived_roles is not None
        assert retrived_user is not None
        assert len(retrived_roles) == 2
        assert len(retrived_user.roles) == 2

    def test_delete_user_does_not_remove_role(self):
        users = UserFactory.create_batch(3)
        user_ids = [user.id for user in users]
        role = RoleFactory()
        role.users = users
        role.save()
        users[0].delete()
        retrived_role = Role.get_by_id(role.id)
        retrived_users = User.query.filter(User.id.in_(user_ids)).all()

        assert retrived_role is not None
        assert retrived_users is not None
        assert len(retrived_users) == 2
        assert len(retrived_role.users) == 2

    def test_role_user_bridge_cascades_on_delete(self):
        user1 = UserFactory()
        user2 = UserFactory()
        roles = RoleFactory.create_batch(3)
        user1.roles = roles
        user2.roles = roles
        user1.save()
        user2.save()
        user1.delete()
        roles[0].delete()

        users_in_bridge = User.query.join(role_user_bridge).join(Role).all()
        roles_in_bridge = Role.query.join(role_user_bridge).join(User).all()

        assert roles_in_bridge is not None
        assert users_in_bridge is not None
        assert len(roles_in_bridge) == 2
        assert len(users_in_bridge) == 1
