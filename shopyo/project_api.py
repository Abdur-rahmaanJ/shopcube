from models import Settings
from app import app


def get_setting(name):
    with app.app_context():
        s = Settings.query.get(name)
        return s.value

base_context = {
    'OUR_APP_NAME': get_setting('OUR_APP_NAME'),
    'SECTION_NAME': get_setting('SECTION_NAME'),
    'SECTION_ITEMS': get_setting('SECTION_ITEMS')
}
