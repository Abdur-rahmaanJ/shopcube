"""
All initialisations like db = SQLAlchemy in this file
"""

from flask_login import LoginManager
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_uploads import IMAGES
from flask_uploads import UploadSet
from flask_mailman import Mail

db = SQLAlchemy()
ma = Marshmallow()
login_manager = LoginManager()
migrate = Migrate()
mail = Mail()