import os

base_path = os.path.dirname(os.path.abspath(__file__))


class Config:
    """Parent configuration class."""

    DEBUG = False
    SQLALCHEMY_DATABASE_URI = "sqlite:///shopyo.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.urandom(24)
    BASE_DIR = base_path
    STATIC = os.path.join(BASE_DIR, "static")
    UPLOADED_PATH_IMAGE = os.path.join(STATIC, "uploads", "images")
    UPLOADED_PATH_THUM = os.path.join(STATIC, "uploads", "thumbs")

    UPLOADED_PRODUCTPHOTOS_DEST = os.path.join(STATIC, "uploads", "products")
    UPLOADED_CATEGORYPHOTOS_DEST = os.path.join(STATIC, "uploads", "category")
    UPLOADED_SUBCATEGORYPHOTOS_DEST = os.path.join(
        STATIC, "uploads", "subcategory"
    )
    PASSWORD_SALT = 'abcdefghi'


class DevelopmentConfig(Config):
    """Configurations for development"""

    ENV = "development"
    DEBUG = True
    EXPLAIN_TEMPLATE_LOADING = True
    LOGIN_DISABLED = True


class TestingConfig(Config):
    """Configurations for testsing"""

    SQLALCHEMY_DATABASE_URI = "sqlite:///testing.db"
    DEBUG = True
    LIVESERVER_PORT = 8943
    LIVESERVER_TIMEOUT = 10

    BCRYPT_LOG_ROUNDS = 4
    TESTING = True
    WTF_CSRF_ENABLED = False


app_config = {
    "development": DevelopmentConfig,
    "production": Config,
    "testing": TestingConfig,
}
