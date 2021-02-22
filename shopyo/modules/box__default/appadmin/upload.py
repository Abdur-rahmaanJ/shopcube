import json
import datetime
from app import app
from modules.box__default.auth.models import User

SEP_CHAR = "#"
SEP_NUM = 23


def add_admin(email, password):
    with app.app_context():
        user = User()
        user.email = email
        user.password = password
        user.is_admin = True
        user.is_email_confirmed = True
        user.email_confirm_date = datetime.datetime.now()
        user.save()


def upload():
    with open("config.json", "r") as config:
        config = json.load(config)
        print("Initialising User")
        print(SEP_CHAR * SEP_NUM, end="\n\n")
        print("Adding Admin ...")
        add_admin(
            config["admin_user"]["email"], config["admin_user"]["password"]
        )
