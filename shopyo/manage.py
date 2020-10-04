import sys

from flask_migrate import Migrate
from flask_migrate import MigrateCommand
from flask_script import Manager

from shopyoapi.init import db
from app import app

from shopyoapi.cmd import clean
from shopyoapi.cmd import initialise
from shopyoapi.cmd import create_module
from shopyoapi.database import autoload_models

migrate = Migrate(app, db, compare_type=True)
manager = Manager(app)

manager.add_command("db", MigrateCommand)


def runserver():
    app.run()


def rundebug():
    app.run(debug=True, host="0.0.0.0")


def custom_commands(args):
    # non migration commands
    if args[1] != "db":
        if args[1] == "initialise":
            autoload_models()
            initialise()
        elif args[1] == "clean":
            clean()
        elif args[1] == "runserver":
            runserver()
        elif args[1] == "rundebug":
            rundebug()
        elif args[1] == "test":
            print("test ok")
        elif args[1] == 'startapp' and args[2]:
            create_module(args[2])
        sys.exit()
    elif args[1] == "db":
        autoload_models()


if __name__ == "__main__":
    custom_commands(sys.argv)
    manager.run()
