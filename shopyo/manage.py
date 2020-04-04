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


with open('config.json', 'r') as config:
    config = json.load(config)


migrate = Migrate(app, db, compare_type=True)
manager = Manager(app)

manager.add_command('db', MigrateCommand)


@manager.command
def initialise():
    print('Creating Db')
    print('#######################')
    subprocess.run([
        sys.executable, 'manage.py', 'db', 'init'
    ], stdout=subprocess.PIPE)
    print('Migrating')
    print('#######################')
    subprocess.run([
        sys.executable, 'manage.py', 'db', 'migrate'
    ], stdout=subprocess.PIPE)
    subprocess.run([
        sys.executable, 'manage.py', 'db', 'upgrade'
    ], stdout=subprocess.PIPE)

    print('Initialising User')
    print('#######################')
    add_admin(config['user']['id'], config['user']['name'],
              config['user']['password'], config['user']['admin'])

    print('Initialising Settings')
    print('#######################')
    for name, value in config['settings'].items():
        add_setting(name, value)
    print('Done!')


@manager.command
def runserver():
    app.run()


@manager.command
def rundebug():
    app.run(debug=True, host='0.0.0.0')


def clean():
    if os.path.exists('test.db'):
        os.remove('test.db')
        print("test.db successfully deleted")
    else:
        print("test.db doesn't exist")
    if os.path.exists('__pycache__'):
        shutil.rmtree('__pycache__')
        print("__pycache__ successfully deleted")
    else:
        print("__pycache__ doesn't exist")
    if os.path.exists('migrations'):
        shutil.rmtree('migrations')
        print("migrations successfully deleted")
    else:
        print("migrations folder doesn't exist")


if __name__ == '__main__':
    manager.run()
