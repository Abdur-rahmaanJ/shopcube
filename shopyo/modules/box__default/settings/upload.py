import json
from app import app
from init import db
from modules.box__default.settings.models import Settings

SEP_CHAR = "#"
SEP_NUM = 23


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


def upload():
    with open("config.json", "r") as config:
        config = json.load(config)
        print("Initialising Settings")
        print(SEP_CHAR * SEP_NUM, end="\n\n")
        print("Adding Dummy Settings ...")
        for name, value in config["settings"].items():
            add_setting(name, value)
