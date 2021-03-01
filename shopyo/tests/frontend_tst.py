import time

from flask_testing import LiveServerTestCase
from selenium import webdriver

from app import create_app

from init import db

from modules.box__default.auth.models import User
from modules.box__default.settings.models import Settings

options = webdriver.ChromeOptions()
options.add_argument("--headless")
options.add_argument("--disable-gpu")

test_user = {"username": "admin", "password": "admin"}


test_user2 = {"username": "test_user", "password": "test_user"}


class TestBase(LiveServerTestCase):
    """Base for frontend testing"""

    def create_app(self):
        config_name = "testing"
        app = create_app(config_name)
        return app

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app(config_name="testing")
        self.client = self.app.test_client
        self.driver = webdriver.Chrome("chromedriver")
        # self.driver.get(self.get_server_url())driver.current_url

        with self.app.app_context():
            # create all tables
            db.create_all()
        setting1 = Settings(setting="APP_NAME", value="Testing")
        setting2 = Settings(setting="SECTION_NAME", value="Category")
        setting3 = Settings(setting="SECTION_ITEMS", value="Products")
        db.session.add_all([setting1, setting2, setting3])
        db.session.commit()

    def tearDown(self):
        """teardown all initialized variables."""
        self.driver.quit()

        with self.app.app_context():
            # drop all tables
            db.session.remove()
            db.drop_all()


class LoginTest(TestBase):
    """Test login"""

    def setUp(self):
        super(LoginTest, self).setUp()
        self.url = f"{self.get_server_url()}/login/"

    def test_successful_login(self):
        user = User()
        user.username = test_user2["username"]
        user.set_hash(test_user2["password"])
        user.admin_user = True
        user.insert()
        self.driver.get(self.url)
        self.driver.find_element_by_id("username").send_keys(
            test_user2["username"]
        )
        self.driver.find_element_by_id("password").send_keys(
            test_user2["password"]
        )
        self.driver.find_element_by_id("submit").click()
        time.sleep(3)
        self.assertEqual(
            self.driver.current_url, "http://localhost:8943/dashboard/"
        )

    def test_failed_login(self):
        self.driver.get(self.url)
        self.driver.find_element_by_id("username").send_keys(
            test_user2["username"]
        )
        self.driver.find_element_by_id("password").send_keys("wrong_password")
        self.driver.find_element_by_id("submit").click()
        time.sleep(3)
        error_message = self.driver.find_element_by_id("error").text
        self.assertEqual(self.driver.current_url, self.url)
        self.assertEqual(
            error_message, "please check your user id and password"
        )
