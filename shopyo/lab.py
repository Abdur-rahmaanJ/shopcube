from werkzeug.security import generate_password_hash, check_password_hash
from models import Users

from flaksqlalchemy.sqlalchemy import  create_engine
from flaksqlalchemy.sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///test.db')
engine.connect()
Session = sessionmaker(bind=engine)
session = Session()

user = Users(id='user', name='Super User',
                 password=generate_password_hash('pass', method='sha256'),
                 admin_user=True)
session.add(user)
session.commit()