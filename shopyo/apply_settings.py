from models import db, Settings
from settings import *

def add_setting(name, value):
    s = Settings(setting=name, value=value)
    db.session.add(s)
    db.session.commit()

# Defined in settings.py
add_setting('OUR_APP_NAME', OUR_APP_NAME)
add_setting('SECTION_NAME', SECTION_NAME)
add_setting('SECTION_ITEMS', SECTION_ITEMS)