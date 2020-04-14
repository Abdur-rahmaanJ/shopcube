import os
import shutil
import sys
import subprocess
import json

from shopyoapi.utils import trycopytree
from shopyoapi.utils import trycopy
from shopyoapi.utils import trymkdir
from shopyoapi.uploads import add_admin
from shopyoapi.uploads import add_setting


def new_project(path, newfoldername):
    print("creating new project {}".format(newfoldername))

    base_path = path + "/" + newfoldername
    trymkdir(base_path)
    """
    if os.path.exists(base_path):
        
    else:
        print('invalid path:', path); sys.exit()"""

    trycopytree("./static", base_path + "/static")
    trycopytree("./tests", base_path + "/tests")
    trycopytree("./modules/base", base_path + "/modules/base")

    trycopy("addon.py", base_path + "/addon.py")
    trycopy("app.py", base_path + "/app.py")
    trycopy("config.json", base_path + "/config.json")
    trycopy("config.py", base_path + "/config.py")
    trycopy("initialise.py", base_path + "/initialise.py")
    trycopy("manage.py", base_path + "/manage.py")
    trycopy("project_api.py", base_path + "/project_api.py")


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


# @manager.command
def initialise():
    with open("config.json", "r") as config:
        config = json.load(config)
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
