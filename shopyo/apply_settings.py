from addon import db
from app import app 
from models import Settings
from settings import *
#from app import db

def add_setting(name, value):
	with app.app_context():
	    if Settings.query.filter_by(setting=name).first():
	        s = Settings.query.get(name)
	        s.value = value
	        db.session.commit()
	    else:
	        s = Settings(setting=name, value=value)
	        db.session.add(s)
	        db.session.commit()

# Defined in settings.py
add_setting('OUR_APP_NAME', OUR_APP_NAME)
add_setting('SECTION_NAME', SECTION_NAME)
add_setting('SECTION_ITEMS', SECTION_ITEMS)