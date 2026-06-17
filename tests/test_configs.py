"""
test all the different configurations types in
config.py
"""
import pytest


class TestAppConfigs:
    @pytest.mark.parametrize("app_type", ["development"])
    def test_dev_app_config(self, app):

        config = app.config

        assert "ENV" in config
        assert config["ENV"] == "development"
        assert "DEBUG" in config
        assert config["DEBUG"] is True
        assert config["LOGIN_DISABLED"] is not None
        assert "SECRET_KEY" in config
        assert config["SECRET_KEY"] is not None
        assert "SQLALCHEMY_DATABASE_URI" in config
        assert config["SQLALCHEMY_DATABASE_URI"] is not None
        assert config["MAIL_SERVER"] in ["localhost", "console"]
        assert "MAIL_PORT" in config
        assert "MAIL_USERNAME" in config
        assert "MAIL_PASSWORD" in config
        assert "MAIL_DEFAULT_SENDER" in config

    # @pytest.mark.parametrize("app_type", ["production"])
    # def test_prod_app_config(self, app):
    #     """
    #     Test the productions configs. Environment variable
    #     configs(private configs) are loaded from .test.prod.env just
    #     to make sure these are loaded correctly
    #     """
    #     config = app.config

    #     assert "ENV" in config
    #     assert config["ENV"] == "production"
    #     assert "DEBUG" in config
    #     assert config["DEBUG"] is False
    #     assert "SECRET_KEY" in config
    #     assert config["SECRET_KEY"] == "secret"
    #     assert "EMAIL_CONFIRMATION_DISABLED" in config
    #     assert config["MAIL_SERVER"] not in ["localhost", "console"]
    #     assert "MAIL_PORT" in config
    #     assert "MAIL_USERNAME" in config
    #     assert config["MAIL_USERNAME"] == "foo@gmail.com"
    #     assert "MAIL_PASSWORD" in config
    #     assert config["MAIL_PASSWORD"] == "pass"
    #     assert "MAIL_DEFAULT_SENDER" in config
    #     assert config["MAIL_DEFAULT_SENDER"] == "foo@gmail.com"
    #     assert "SQLALCHEMY_DATABASE_URI" in config
    # assert (
    #     config["SQLALCHEMY_DATABASE_URI"]
    #     == "mysql+pymysql://db_username:db_password@db_host/db_name"
    # )
