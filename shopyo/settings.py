from models import Settings

def get_value(name):
    s = Settings.query.get(name)
    return s.value

OUR_APP_NAME = 'Demo'
SECTION_NAME = 'Manufacturers'
SECTION_ITEMS = 'Products'

