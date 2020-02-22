from werkzeug.security import check_password_hash, generate_password_hash

from addon import db
from models import Users
from run import app


def add_admin():
    with app.app_context():
        db.create_all()
        user = Users(
                     id='user',
                     name='Super User',
                     password=generate_password_hash('pass', method='sha256'),
                     admin_user=True)
        db.session.add(user)
        db.session.commit()
