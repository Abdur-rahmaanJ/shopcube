from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_login import LoginManager

db = SQLAlchemy()
ma = Marshmallow()
login_manager = LoginManager()