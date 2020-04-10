class Config:
    """Parent configuration class."""

    DEBUG = False
    SQLALCHEMY_DATABASE_URI = "sqlite:///test.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = "qow32ijjdkc756osk5dmck"  # Need a generator
    APP_NAME = "Demo"
    SECTION_NAME = "Manufacturer"
    SECTION_ITEMS = "Products"
    HOMEPAGE_URL = "/control_panel"


class DevelopmentConfig(Config):
    """Configurations for development"""

    ENV = "development"
    DEBUG = True


class TestingConfig(Config):
    """Configurations for testsing"""

    SQLALCHEMY_DATABASE_URI = "sqlite:///testing.db"
    DEBUG = True


app_config = {
    "development": DevelopmentConfig,
    "production": Config,
    "testing": TestingConfig,
}
