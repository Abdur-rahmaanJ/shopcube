import json

from init import db
from modules.box__default.settings.models import Settings


def add_setting(name, value):
    if Settings.query.filter_by(setting=name).first():
        s = Settings.query.get(name)
        s.value = value
        db.session.commit()
    else:
        s = Settings(setting=name, value=value)
        db.session.add(s)
        db.session.commit()


def upload(verbose=False):
    with open("config.json") as config:
        config = json.load(config)
        for name, value in config["settings"].items():
            add_setting(name, value)

        if verbose:
            print("[x] Added Dummy Settings")
