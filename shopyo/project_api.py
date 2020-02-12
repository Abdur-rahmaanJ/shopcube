from models import Settings


def get_setting(name):
    s = Settings.query.get(name)
    return s.value


def base_context():
    base_context = {
        'OUR_APP_NAME': get_setting('OUR_APP_NAME'),
        'SECTION_NAME': get_setting('SECTION_NAME'),
        'SECTION_ITEMS': get_setting('SECTION_ITEMS')
    }
    return base_context
