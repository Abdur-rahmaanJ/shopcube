import json
import os

import pytest

from app import create_app

from shopyoapi.init import db
from shopyoapi.uploads import add_setting

from modules.admin.models import User
from modules.settings.models import Settings

# from shopyoapi.cmd import initialise

# run in shopyo/shopyo
# python -m pytest .


if os.path.exists("testing.db"):
    os.remove("testing.db")


@pytest.fixture(scope="session")
def new_user():
    user = User(username="abcd")
    user.set_hash("pass")
    return user


@pytest.fixture(scope="session")
def test_client():
    flask_app = create_app("testing")

    # Flask provides a way to test your application by exposing the Werkzeug test Client
    # and handling the context locals for you.
    testing_client = flask_app.test_client()

    # Establish an application context before running the tests.
    ctx = flask_app.app_context()
    ctx.push()

    yield testing_client  # this is where the testing happens!

    ctx.pop()


@pytest.fixture(scope="session")
def init_database():

    # Create the database and the database table
    db.create_all()

    # Insert user data
    user1 = User(username="car")
    user1.set_hash("pass")
    user2 = User(username="field")
    user2.set_hash("pass")
    db.session.add(user1)
    db.session.add(user2)

    with open("config.json", "r") as config:
        config = json.load(config)
    for name, value in config["settings"].items():
        s = Settings(setting=name, value=value)
        db.session.add(s)
    db.session.commit()

    # Commit the changes for the users
    db.session.commit()

    # initialise()
    yield db  # this is where the testing happens!

    # db.drop_all()
