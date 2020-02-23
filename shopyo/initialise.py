from werkzeug.security import check_password_hash, generate_password_hash

from addon import db
from app import app

from views.admin.models import Users
from views.settings.models import Settings


def add_admin(user_id, name, password, admin):
    with app.app_context():
        user = Users(
                 id=user_id,
                 name=name,
                 password=generate_password_hash(password, method='sha256'),
                 admin_user=admin
        )
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
