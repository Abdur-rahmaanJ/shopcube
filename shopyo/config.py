import os

base_path = os.path.dirname(os.path.abspath(__file__))


class BaseConfig:
    """Parent configuration class."""

    DEBUG = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    BASE_DIR = base_path
    STATIC = os.path.join(base_path, "static")
    UPLOADED_PATH_IMAGE = os.path.join(STATIC, "uploads", "images")
    UPLOADED_PATH_THUMB = os.path.join(STATIC, "uploads", "thumbs")


class ProductionConfig(BaseConfig):
    """Configurations for production"""

    # built in flask configs
    ENV = "production"
    SECRET_KEY = os.environ.get("SECRET_KEY")

    # control email confirmation for user registration
    EMAIL_CONFIRMATION_DISABLED = False

    # flask-mailman configs
    MAIL_SERVER = "smtp.googlemail.com"
    MAIL_PORT = 465
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True
    MAIL_USERNAME = os.environ.get("MAIL_USERNAME")
    MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD")
    MAIL_DEFAULT_SENDER = os.environ.get("MAIL_DEFAULT_SENDER")

    # database configs
    SQLALCHEMY_DATABASE_URI = (
        os.environ.get("SQLALCHEMY_DATABASE_URI") or "sqlite:///shopyo.db"
    )


class DevelopmentConfig(BaseConfig):
    """Configurations for development"""

    # built in flask configs
    ENV = "development"
    DEBUG = True
    LOGIN_DISABLED = False
    SECRET_KEY = "secret"

    # control email confirmation for user registration
    EMAIL_CONFIRMATION_DISABLED = False

    # flask-mailman configs
    MAIL_SERVER = "localhost"
    MAIL_PORT = 1025
    MAIL_USE_TLS = False
    MAIL_USE_SSL = False
    MAIL_USERNAME = ""
    MAIL_PASSWORD = ""
    MAIL_DEFAULT_SENDER = "ma@mail.com"

    # database configs
    SQLALCHEMY_DATABASE_URI = "sqlite:///shopyo.db"

    # unknown configs
    PASSWORD_SALT = "some pasword salt"


class TestingConfig(BaseConfig):
    """Configurations for testsing"""

    # built in flask configs
    ENV = "testing"
    TESTING = True
    DEBUG = True
    SERVER_NAME = "localhost.com"
    SECRET_KEY = "secret"
    PREFERRED_URL_SCHEME = "http"

    # flask WTF configs
    WTF_CSRF_ENABLED = False

    # control email confirmation for user registration
    EMAIL_CONFIRMATION_DISABLED = False

    # flask-mailman configs
    MAIL_BACKEND = "console"
    MAIL_USERNAME = "shopyofrom@test.com"
    MAIL_PASSWORD = "pass"
    MAIL_DEFAULT_SENDER = "shopyofrom@test.com"

    # flask sqlalchemy configs
    SQLALCHEMY_DATABASE_URI = "sqlite:///testing.db"

    # flask bycrpt configs
    BCRYPT_LOG_ROUNDS = 4

    # unknown configs
    PASSWORD_SALT = "some pasword salt"
    LIVESERVER_PORT = 8943
    LIVESERVER_TIMEOUT = 10


app_config = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
    "testing": TestingConfig,
}
