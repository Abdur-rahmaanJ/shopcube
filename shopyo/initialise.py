from werkzeug.security import generate_password_hash, check_password_hash
from models import db, Users

if __name__ == '__main__':
    db.create_all()
    user = Users(id = 'user', name = 'Super User',
    	password=generate_password_hash('pass', method='sha256'),admin_user=True)
    db.session.add(user)
    db.session.commit()


