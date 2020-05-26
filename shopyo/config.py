class Config:
    """Parent configuration class."""

    DEBUG = False
    SQLALCHEMY_DATABASE_URI = "sqlite:///test.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = "qow32ijjdkc756osk5dmck"  # Need a generator
    HOMEPAGE_URL = "/control_panel"
    USER_ROLES = ['teacher', 'mailman', 'lawyer', 'doctor']


class DevelopmentConfig(Config):
    """Configurations for development"""

    ENV = "development"
    DEBUG = True


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
