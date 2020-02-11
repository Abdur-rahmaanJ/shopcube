from models import Settings

def get_value(name):
    s = Settings.query.get(name)
    return s.value

SQLALCHEMY_DATABASE_URI = 'sqlite:///test.db'

SQLALCHEMY_TRACK_MODIFICATIONS = False

SECRET_KEY = 'qow32ijjdkc756osk5dmck'  # Need a generator


OUR_APP_NAME = 'Demo'
SECTION_NAME = 'Manufacturer'
SECTION_ITEMS = 'Products'

HOMEPAGE_URL = '/manufac/'


