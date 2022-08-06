"""
All initialisations like db = SQLAlchemy in this file
"""

from flask_login import LoginManager
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_uploads import IMAGES
from flask_uploads import UploadSet

db = SQLAlchemy()
ma = Marshmallow()
login_manager = LoginManager()
migrate = Migrate()

productphotos = UploadSet("productphotos", IMAGES)
categoryphotos = UploadSet("categoryphotos", IMAGES)
subcategoryphotos = UploadSet("subcategoryphotos", IMAGES)
