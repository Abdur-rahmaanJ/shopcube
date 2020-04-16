import unittest

from app import create_app
from shopyoapi.init import db


class BaseTest(unittest.TestCase):
    """Base test class"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app(config_name="testing")
        self.client = self.app.test_client

        with self.app.app_context():
            # create all tables
            db.create_all()

    def tearDown(self):
        """teardown all initialized variables."""
        with self.app.app_context():
            # drop all tables
            db.session.remove()
            db.drop_all()
