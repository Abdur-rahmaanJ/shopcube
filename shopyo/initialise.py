from werkzeug.security import generate_password_hash, check_password_hash
from app import app
from addon import db
from models import Users
#from app import db


#if __name__ == '__main__':
def add_admin():
    with app.app_context():
        #db.create_all()
        user = Users(
                     id='user',
                     name='Super User',
                     password=generate_password_hash('pass', method='sha256'),
                     admin_user=True)
        db.session.add(user)
        db.session.commit()

add_admin()