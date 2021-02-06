import datetime
import uuid

from werkzeug.security import generate_password_hash

from app import app
from shopyoapi.init import db
from modules.box__default.admin.models import User
from modules.box__default.settings.models import Settings


def add_admin(email, password):
    with app.app_context():
        user = User()
        user.email = email
        user.password = generate_password_hash(password, method="sha256")
        user.is_admin = True
        user.email_confirmed = True
        user.email_confirm_date = datetime.datetime.now()
        user.save()

def upload(email, password):
    print("Adding Admin ...")
    add_admin(email, password)
