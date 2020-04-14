import json
import os
import shutil
import subprocess
import sys

from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager

from addon import db
from app import app
from initialise import add_admin, add_setting

migrate = Migrate(app, db, compare_type=True)
manager = Manager(app)

manager.add_command("db", MigrateCommand)

with open("config.json", "r") as config:
    config = json.load(config)
# @manager.command
def initialise():

    print("Creating Db")
    print("#######################")
    subprocess.run([sys.executable, "manage.py", "db", "init"], stdout=subprocess.PIPE)
    print("Migrating")
    print("#######################")
    subprocess.run(
        [sys.executable, "manage.py", "db", "migrate"], stdout=subprocess.PIPE
    )
    subprocess.run(
        [sys.executable, "manage.py", "db", "upgrade"], stdout=subprocess.PIPE
    )

    print("Initialising User")
    print("#######################")
    add_admin(
        config["user"]["id"],
        config["user"]["name"],
        config["user"]["password"],
        config["user"]["admin"],
    )

    print("Initialising Settings")
    print("#######################")
    for name, value in config["settings"].items():
        add_setting(name, value)
    print("Done!")


#@manager.command
def runserver():
    app.run()


#@manager.command
def rundebug():
    app.run(debug=True, host="0.0.0.0")


def clean():
    if os.path.exists("test.db"):
        os.remove("test.db")
        print("test.db successfully deleted")
    else:
        print("test.db doesn't exist")
    if os.path.exists("__pycache__"):
        shutil.rmtree("__pycache__")
        print("__pycache__ successfully deleted")
    else:
        print("__pycache__ doesn't exist")
    if os.path.exists("migrations"):
        shutil.rmtree("migrations")
        print("migrations successfully deleted")
    else:
        print("migrations folder doesn't exist")

def new_project(path, newfoldername):
    print('creating new project')
    print('creating dir {} in {}'.format(newfoldername, path))
    base_path = path+'/'+newfoldername
    try:
        os.mkdir(base_path)
    except:
        pass
    '''
    if os.path.exists(base_path):
        
    else:
        print('invalid path:', path); sys.exit()'''
    try:
        shutil.copytree('./static', base_path+'/static')
        shutil.copytree('./tests', base_path+'/tests')

    except:
        pass

    try:
        shutil.copytree('./modules/base', base_path+'/modules/base')
    except Exception as e:
        print(e)

    try:
        shutil.copy('addon.py', base_path+'/addon.py')
        shutil.copy('app.py', base_path+'/app.py')
        shutil.copy('config.json', base_path+'/config.json')
        shutil.copy('config.py', base_path+'/config.py')
        shutil.copy('initialise.py', base_path+'/initialise.py')
        shutil.copy('manage.py', base_path+'/manage.py')
        shutil.copy('project_api.py', base_path+'/project_api.py')
    except:
        pass


def custom_commands(args):
    # non migration commands
    if args[1] != 'db':
        if args[1] == 'initialise':
            initialise()
        elif args[1] == 'clean':
            clean()
        elif args[1] == 'runserver':
            runserver()
        elif args[1] == 'rundebug':
            rundebug()
        elif args[1] == 'test':
            print('test ok')
        elif args[1] == 'new' and args[2] and args[3]:
            new_project(args[2], args[3])
        sys.exit()

if __name__ == "__main__":
    custom_commands(sys.argv)
    manager.run()

