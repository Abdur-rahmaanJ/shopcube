"""
All initialisations like db = SQLAlchemy in this file
"""

import os

from flask_login import LoginManager
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_uploads import IMAGES
from flask_uploads import UploadSet
from flask_mailman import Mail


import os

root_path = os.path.dirname(os.path.abspath(__file__)) # don't remove
static_path = os.path.join(root_path, "static") # don't remove
modules_path = os.path.join(root_path, "modules") # don't remove
themes_path = os.path.join(static_path, "themes") # don't remove

db = SQLAlchemy()
ma = Marshmallow()
login_manager = LoginManager()
migrate = Migrate()
mail = Mail()