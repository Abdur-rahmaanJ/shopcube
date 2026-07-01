"""
File conftest.py contains pytest fixtures that are used in numerous
test functions. Refer to https://docs.pytest.org/en/stable/fixture.html
for more details on pytest
"""
import datetime
import json
import os
import sys

# Ensure the shopcube directory (containing the real app.py) is first on sys.path
# so `from app import create_app` imports THIS project's app.py, not a stray
# app.py in a parent directory.
_THIS_DIR = os.path.dirname(os.path.abspath(__file__))
if _THIS_DIR not in sys.path:
    sys.path.insert(0, _THIS_DIR)
elif sys.path[0] != _THIS_DIR:
    sys.path.remove(_THIS_DIR)
    sys.path.insert(0, _THIS_DIR)

# Add packages/shopyo_ecommerce dir so local shopyo_ecommerce takes precedence
# over the PyPI-installed version when tests import it.
_PACKAGES_DIR = os.path.join(_THIS_DIR, "packages", "shopyo_ecommerce")
if _PACKAGES_DIR not in sys.path:
    sys.path.insert(0, _PACKAGES_DIR)

import pytest
from app import create_app
from flask import url_for
from flask_login import current_user as _current_user
from init import db as _db
from shopyo_auth.models import User
from shopyo_settings.models import Settings
from sqlalchemy import event

# Import all ecommerce models so SQLAlchemy can resolve string-based relationships
import shopyo_ecommerce.resource.models  # noqa: F401, E402
import shopyo_ecommerce.product.models  # noqa: F401, E402
import shopyo_ecommerce.category.models  # noqa: F401, E402
import shopyo_ecommerce.vendor.models  # noqa: F401, E402
import shopyo_ecommerce.customer.models  # noqa: F401, E402
import shopyo_ecommerce.inventory.models  # noqa: F401, E402
import shopyo_ecommerce.pos.models  # noqa: F401, E402
import shopyo_ecommerce.purchase.models  # noqa: F401, E402
import shopyo_ecommerce.shop.models  # noqa: F401, E402
import shopyo_ecommerce.shopman.models  # noqa: F401, E402

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
    user.fixture_email = "unconfirmed@domain.com"
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
    user.fixture_email = "admin1@domain.com"
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
    user.fixture_email = "admin2@domain.com"
    return user


@pytest.fixture(scope="session")
def flask_app():
    flask_app = create_app("testing")
    return flask_app


@pytest.fixture(scope="session")
def app(request):
    """
    Returns session-wide application.
    """
    return create_app("testing")


@pytest.fixture(scope="session")
def current_user():
    return _current_user


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
    with open("config.json") as config:
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
    try:
        session = db._make_scoped_session(options=options)
    except:
        session = db.create_scoped_session(options=options)
    db.session = session

    yield session

    transaction.rollback()
    connection.close()
    session.remove()


# @pytest.fixture(scope="function", autouse=True)
# def db_session(app, db, request):
#     """
#     Returns function-scoped session.
#     """
#     with app.app_context():
#         conn = _db.engine.connect()
#         txn = conn.begin()

#         options = dict(bind=conn, binds={})
#         sess = _db.create_scoped_session(options=options)

#         # establish  a SAVEPOINT just before beginning the test
#         # (http://docs.sqlalchemy.org/en/latest/orm/session_transaction.html#using-savepoint)
#         sess.begin_nested()

#         @event.listens_for(sess(), "after_transaction_end")
#         def restart_savepoint(sess2, trans):
#             # Detecting whether this is indeed the nested transaction of the test
#             if trans.nested and not trans._parent.nested:
#                 # The test should have normally called session.commit(),
#                 # but to be safe we explicitly expire the session
#                 sess2.expire_all()
#                 sess.begin_nested()

#         _db.session = sess
#         yield sess

#         # Cleanup
#         sess.remove()
#         # This instruction rollsback any commit that were executed in the tests.
#         txn.rollback()
#         conn.close()


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
        email = getattr(user, "fixture_email", None) or user.email
        return self._client.post(
            url_for("shopyo_auth.login"),
            data=dict(email=email, password=password),
            follow_redirects=True,
        )

    def logout(self):
        return self._client.get(url_for("shopyo_auth.logout"), follow_redirects=True)


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
