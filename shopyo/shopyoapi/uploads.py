from werkzeug.security import generate_password_hash

from shopyoapi.init import db
from app import app

from modules.admin.models import Users
from modules.settings.models import Settings


def add_admin(username, password, admin):
    with app.app_context():
        user = Users()
        user.username = username
        user.password = generate_password_hash(password, method="sha256")
        user.admin_user = admin
        db.session.add(user)
        db.session.commit()


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
