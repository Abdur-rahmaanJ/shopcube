"""
File conftest.py contains pytest fixtures that are used in numerous
test functions. Refer to https://docs.pytest.org/en/stable/fixture.html
for more details on pytest
"""
import json
import os
import pytest
import datetime
from flask import url_for

from app import create_app
from init import db as _db
from modules.box__default.auth.models import User
from modules.box__default.settings.models import Settings

# run in shopyo/shopyo
# python -m pytest . or python -m pytest -v

if os.path.exists("testing.db"):
    os.remove("testing.db")


@pytest.fixture(scope="session")
def unconfirmed_user():
    """
    A pytest fixture that returns a non admin user
    """
    user = User()
    user.email = "unconfirmed@domain.com"
    user.password = "pass"
    user.is_email_confirmed = False
    return user


@pytest.fixture(scope="session")
def non_admin_user():
    """
    A pytest fixture that returns a non admin user
    """
    user = User()
    user.email = "admin1@domain.com"
    user.password = "pass"
    user.is_email_confirmed = True
    user.email_confirm_date = datetime.datetime.now()
    return user


@pytest.fixture(scope="session")
def admin_user():
    """
    A pytest fixture that returns an admin user
    """
    user = User()
    user.email = "admin2@domain.com"
    user.password = "pass"
    user.is_admin = True
    user.is_email_confirmed = True
    user.email_confirm_date = datetime.datetime.now()
    return user


@pytest.fixture(scope="session")
def flask_app():
    flask_app = create_app("testing")
    return flask_app


@pytest.fixture(scope="session")
def test_client(flask_app):
    """
    setups up and returns the flask testing app
    """
    # Create a test client using the Flask application configured for testing
    with flask_app.test_client() as testing_client:
        # Establish an application context
        with flask_app.app_context():
            yield testing_client  # this is where the testing happens!


@pytest.fixture(scope="session")
def db(test_client, non_admin_user, admin_user, unconfirmed_user):
    """
    creates and returns the initial testing database
    """
    # Create the database and the database table
    _db.app = test_client
    _db.create_all()

    # Insert admin, non admin, and unconfirmed
    _db.session.add(non_admin_user)
    _db.session.add(admin_user)
    _db.session.add(unconfirmed_user)

    # add the default settings
    with open("config.json", "r") as config:
        config = json.load(config)
    for name, value in config["settings"].items():
        s = Settings(setting=name, value=value)
        _db.session.add(s)

    # Commit the changes for the users
    _db.session.commit()

    yield _db  # this is where the testing happens!

    _db.drop_all()


@pytest.fixture(scope="function", autouse=True)
def db_session(db):
    """
    Creates a new database session for a test. Note you must use this fixture
    if your test connects to db. Autouse is set to true which implies
    that the fixture will be setup before each test

    Here we not only support commit calls but also rollback calls in tests.
    """
    connection = db.engine.connect()
    transaction = connection.begin()
    options = dict(bind=connection, binds={})
    session = db.create_scoped_session(options=options)
    db.session = session

    yield session

    transaction.rollback()
    connection.close()
    session.remove()


@pytest.fixture
def login_unconfirmed_user(auth, unconfirmed_user):
    """Login with unconfirmed and logout during teadown"""
    auth.login(unconfirmed_user)
    yield
    auth.logout()


@pytest.fixture
def login_admin_user(auth, admin_user):
    """Login with admin and logout during teadown"""
    auth.login(admin_user)
    yield
    auth.logout()


@pytest.fixture
def login_non_admin_user(auth, non_admin_user):
    """Login with non-admin and logout during teadown"""
    auth.login(non_admin_user)
    yield
    auth.logout()


@pytest.fixture
def auth(test_client):
    return AuthActions(test_client)


class AuthActions:
    def __init__(self, client):
        self._client = client

    def login(self, user, password="pass"):
        return self._client.post(
            url_for("auth.login"),
            data=dict(email=user.email, password=password),
            follow_redirects=True,
        )

    def logout(self):
        return self._client.get(url_for("auth.logout"), follow_redirects=True)


# Want TO USE THE BELOW 2 FIXTURES TO DYNAMICALLY
# GET THE ROUTES FOR A GIVEN MODULE BUT UNABLE TO
# PARAMETERIZE THE LIST OF ROUTES RETURNED FROM THE FIXTURE
# CURRENTLY THIS NOT POSSIBLE WITH FIXTURES IN PYTEST @rehmanis

# @pytest.fixture(scope="module")
# def get_module_routes(request, get_routes):
#     module_prefix = getattr(request.module, "module_prefix", "/")
#     return get_routes[module_prefix]


# @pytest.fixture(scope="session")
# def get_routes(flask_app):

#     routes_dict = {}
#     relative_path = "/"
#     prefix = "/"

#     for route in flask_app.url_map.iter_rules():
#         split_route = list(filter(None, str(route).split("/", 2)))

#         if len(split_route) == 0:
#             prefix = "/"
#             relative_path = ""
#         elif len(split_route) == 1:
#             prefix = "/" + split_route[0]
#             relative_path = "/"
#         else:
#             prefix = "/" + split_route[0]
#             relative_path = split_route[1]

#         if prefix in routes_dict:
#             routes_dict[prefix].append(relative_path)
#         else:
#             routes_dict[prefix] = [relative_path]

#     return routes_dict
