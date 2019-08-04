import os
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager

from app import app
from models import db


#app.config.from_object(os.environ['APP_SETTINGS'])

migrate = Migrate(app, db, compare_type=True)
manager = Manager(app)

manager.add_command('db', MigrateCommand)


if __name__ == '__main__':
    manager.run()