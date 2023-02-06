import datetime
import json

from modules.box__default.auth.models import User


def add_admin(email, password):
    user = User()
    user.email = email
    user.password = password
    user.is_admin = True
    user.is_email_confirmed = True
    user.email_confirm_date = datetime.datetime.now()
    user.save()


def upload(verbose=False):
    with open("config.json") as config:
        config = json.load(config)
        add_admin(config["admin_user"]["email"], config["admin_user"]["password"])

        if verbose:
            print("[x] Added Admin User")
