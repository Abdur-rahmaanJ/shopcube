import os
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager

from run import app
from models import db

from initialise import add_admin

#app.config.from_object(os.environ['APP_SETTINGS'])

migrate = Migrate(app, db, compare_type=True)
manager = Manager(app)

manager.add_command('db', MigrateCommand)

@manager.command
def initialise():
    add_admin()

@manager.command
def runserver():
    app.run()

@manager.command
def rundebug():
    app.run(debug=True)

if __name__ == '__main__':
    manager.run()