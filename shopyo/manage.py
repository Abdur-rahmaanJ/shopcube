import os
import json
import shutil
import sys
import subprocess


from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from initialise import add_admin, add_setting
from app import app

from addon import db



#app.config.from_object(os.environ['APP_SETTINGS'])

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

@manager.command
def clean():
    if os.path.exists('test.db'):
        os.remove('test.db')
        print("The file was successfully deleted")
    else:
        print("The file doesn't exist")
    if os.path.exists('__pycache__'):
        shutil.rmtree('__pycache__')
        print("The directory was successfully deleted")
    else:
        print("The directory doesn't exist")
    if os.path.exists('migrations'):
        shutil.rmtree('migrations')
        print("The directory was successfully deleted")
    else:
        print("The directory doesn't exist")


if __name__ == '__main__':
    manager.run()
