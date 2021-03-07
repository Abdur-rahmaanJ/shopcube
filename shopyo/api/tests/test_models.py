"""
Tests all db utilities such as CRUDMixin defined under shopapi/models.py
Most of the test cases taken from:
https://github.com/cookiecutter-flask/cookiecutter-flask
"""

import pytest
from flask_login import UserMixin
from init import db
from shopyo.api.models import PkModel


class ExampleUserModel(PkModel, UserMixin):
    """Example user model for testing purposes"""

    __tablename__ = "testusers"

    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)


class TestPKModel:
    """Tests all functions of PKModel"""

    def test_get_by_id(self):
        result = ExampleUserModel.get_by_id("myId")

        assert not result

    def test_get_by_id_valid(self, db_session):
        user_bar = ExampleUserModel(username="bar", email="bar@domain.com")
        user_foo = ExampleUserModel(username="foo", email="foo@domain.com")
        user_bar.save()
        user_foo.save()
        result_int = ExampleUserModel.get_by_id(user_bar.id)
        result_str = ExampleUserModel.get_by_id(str(user_bar.id))
        expected = (
            db_session.query(ExampleUserModel)
            .filter(ExampleUserModel.username == "bar")
            .scalar()
        )

        assert result_int
        assert expected
        assert result_int.username == expected.username
        assert result_str.username == expected.username


class TestCRUDMixin:
    """Test class for testing all CRUD functions"""

    def test_create(self, db_session):
        user = ExampleUserModel.create(username="bar", email="bar@domain.com")
        result_raw = db_session.execute(
            """select * from testusers"""
        ).fetchone()
        result_orm = (
            db_session.query(ExampleUserModel)
            .filter(ExampleUserModel.id == user.id)
            .scalar()
        )

        assert result_orm
        assert result_raw
        assert result_raw.username == "bar"
        assert result_orm.username == "bar"

    @pytest.mark.parametrize(
        "commit,expected", [(True, "foo"), (False, "bar")]
    )
    def test_update_single(self, db_session, commit, expected):
        user = ExampleUserModel(username="bar", email="bar@domain.com")
        user.save()
        user.update(commit=commit, username="foo")
        result = db_session.execute("""select * from testusers""").fetchone()

        assert result
        assert result.username == expected

    @pytest.mark.parametrize(
        "commit,expected",
        [
            (True, {"username": "foo", "email": "foo@domain.com"}),
            (False, {"username": "bar", "email": "bar@domain.com"}),
        ],
    )
    def test_update_multiple(self, db_session, commit, expected):
        user = ExampleUserModel(username="bar", email="bar@domain.com")
        user.save()
        user.update(commit=commit, username="foo", email="foo@domain.com")
        result = db_session.execute("""select * from testusers""").fetchone()

        assert result
        assert result.username == expected["username"]
        assert result.email == expected["email"]

    @pytest.mark.parametrize("commit,expected", [(True, None), (False, "bar")])
    def test_delete(self, commit, expected):
        user = ExampleUserModel(username="bar", email="bar@domain.com")
        user.save()
        user.delete(commit=commit)
        result = ExampleUserModel.get_by_id(user.id)
        if result:
            result = result.username

        assert result == expected
