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
    user = User(email="admin3@domain.com")
    user.set_hash("pass")
    return user


@pytest.fixture(scope="session")
def test_client():
    flask_app = create_app("testing")

    # Create a test client using the Flask application configured for testing
    # we need this with block to be able to use application context
    with flask_app.test_client() as testing_client:
        # Establish an application context
        with flask_app.app_context():
            yield testing_client  # this is where the testing happens!


@pytest.fixture(scope="session")
def init_database():

    # Create the database and the database table
    db.create_all()

    # Insert user data
    user1 = User(email="admin1@domain.com")
    user1.set_hash("pass")
    user2 = User(email="admin2@domain.com", is_admin=True)
    user2.set_hash("pass")
    db.session.add(user1)
    db.session.add(user2)

    with open("config.json", "r") as config:
        config = json.load(config)
    for name, value in config["settings"].items():
        s = Settings(setting=name, value=value)
        db.session.add(s)

    # Commit the changes for the users
    db.session.commit()

    # initialise()
    yield db  # this is where the testing happens!

    # db.drop_all()
