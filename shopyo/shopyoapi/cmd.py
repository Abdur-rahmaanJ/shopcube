import os
import shutil
import sys
import subprocess
import json

from shopyoapi.utils import trycopytree
from shopyoapi.utils import trycopy
from shopyoapi.utils import trymkdir
from shopyoapi.utils import trymkfile
from shopyoapi.uploads import add_admin
from shopyoapi.uploads import add_setting


def new_project(path, newfoldername):
    newfoldername = newfoldername.strip('/').strip('\\')
    print("creating new project {}".format(newfoldername))

    base_path = path + "/" + newfoldername
    trymkdir(base_path)
    print("created dir {} in {}".format(newfoldername, path))

    trycopytree("./static", base_path + "/static")
    trycopytree("./tests", base_path + "/tests")
    trycopytree("./modules/base", base_path + "/modules/base")
    trycopytree("./modules/admin", base_path + "/modules/admin")
    trycopytree("./modules/login", base_path + "/modules/login")
    trycopytree("./modules/settings", base_path + "/modules/settings")
    trycopytree("./shopyoapi", base_path + "/shopyoapi")

    trycopy("app.py", base_path + "/app.py")
    trycopy("config.json", base_path + "/config.json")
    trycopy("config.py", base_path + "/config.py")
    trycopy("manage.py", base_path + "/manage.py")


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


def initialise():
    with open("config.json", "r") as config:
        config = json.load(config)
    print("Creating Db")
    print("#######################")
    subprocess.run(
        [sys.executable, "manage.py", "db", "init"], stdout=subprocess.PIPE
    )
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
        config["admin_user"]["name"],
        config["admin_user"]["password"]
    )

    print("Initialising Settings")
    print("#######################")
    for name, value in config["settings"].items():
        add_setting(name, value)
    print("Done!")


def create_module(modulename):
    print('creating module: {}'.format(modulename))
    base_path = 'modules/' + modulename
    trymkdir(base_path)
    trymkdir(base_path+'/templates')
    trymkdir(base_path+'/templates/'+modulename)
    view_content = '''
from flask import Blueprint
{0}_blueprint = Blueprint(
    "{0}",
    __name__,
    url_prefix='/{0}',
    template_folder="templates",
)


@{0}_blueprint.route("/")
def index():
    return ''
'''.format(modulename)
    trymkfile(base_path+'/'+'view.py', view_content)
    trymkfile(base_path+'/'+'forms.py', '')
    trymkfile(base_path+'/'+'models.py', '')
    info_json_content = '''{{
        "name": "{}",
        "type": "show",
        "fa-icon": "fa fa-store",
        "url_prefix": "/{}"
}}'''.format(modulename.capitalize(), modulename)
    trymkfile(base_path+'/'+'info.json', info_json_content)
