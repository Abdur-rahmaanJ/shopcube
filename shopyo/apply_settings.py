from models import db, Settings
from settings import *

def add_setting(name, value):
    s = Settings(setting=name, value=value)
    db.session.add(s)
    db.session.commit()

add_setting('OUR_APP_NAME', OUR_APP_NAME)