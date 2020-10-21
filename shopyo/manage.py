import sys
import argparse

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
    parser = argparse.ArgumentParser(description="Process some argument.")
    parser.add_argument("action", nargs="+", help="db or other actions")
    args = parser.parse_args()
    # non migration commands
    if args.action[0] != "db":
        if args.action[0] == "initialise":
            autoload_models()
            initialise()
        elif args.action[0] == "clean":
            clean()
        elif args.action[0] == "runserver":
            runserver()
        elif args.action[0] == "rundebug":
            rundebug()
        elif args.action[0] == "test":
            print("test ok")
        elif args.action[0] == "startapp" and args.action[1]:
            create_module(args.action[1])
        sys.exit()
    elif args.action[0] == "db":
        pass


if __name__ == "__main__":
    custom_commands(sys.argv)
    autoload_models()
    manager.run()
