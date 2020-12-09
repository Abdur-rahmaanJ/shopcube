import json
import os
import re
import shutil
import subprocess
import sys

from shopyoapi.uploads import add_admin
from shopyoapi.uploads import add_setting
from shopyoapi.uploads import add_uncategorised_category

# from .file import trycopytree
# from .file import trycopy
from .file import trymkdir
from .file import trymkfile


def clean():
    """
    cleans shopyo.db __pycache__ and migrations/

    Parameters
    ----------


    Returns
    -------
    None
        ...

    """
    if os.path.exists("shopyo.db"):
        os.remove("shopyo.db")
        print("shopyo.db successfully deleted")
    else:
        print("shopyo.db doesn't exist")
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
    """
    Create db, migrate, adds default users, add settings

    Parameters
    ----------


    Returns
    -------
    None


    """
    SEP_CHAR = "#"
    SEP_NUM = 23

    with open("config.json", "r") as config:
        config = json.load(config)

    print("Creating Db")
    print(SEP_CHAR * SEP_NUM, end="\n\n")
    subprocess.run([sys.executable, "manage.py", "db", "init"], stdout=subprocess.PIPE)

    print("Migrating")
    print(SEP_CHAR * SEP_NUM, end="\n\n")
    subprocess.run(
        [sys.executable, "manage.py", "db", "migrate"], stdout=subprocess.PIPE
    )
    subprocess.run(
        [sys.executable, "manage.py", "db", "upgrade"], stdout=subprocess.PIPE
    )

    print("Initialising User")
    print(SEP_CHAR * SEP_NUM, end="\n\n")
    add_admin(config["admin_user"]["email"], config["admin_user"]["password"])

    print("Initialising Settings")
    print(SEP_CHAR * SEP_NUM, end="\n\n")
    for name, value in config["settings"].items():
        add_setting(name, value)

    print("Adding category and subcategory: uncategorised")
    print(SEP_CHAR * SEP_NUM, end="\n\n")
    add_uncategorised_category()

    print("Done!")


def create_module(modulename):
    """
    creates module with the structure defined in the modules section in docs

    Parameters
    ----------
    modulename: str
        name of module, in alphanumeric-underscore

    Returns
    -------
    None


    """

    if bool(re.match(r"^[A-Za-z0-9_]+$", modulename)) is False:
        print(
            "Error: modulename is not valid, please use alphanumeric and underscore only"
        )
        sys.exit()
    print("creating module: {}".format(modulename))
    base_path = "modules/" + modulename
    trymkdir(base_path)
    trymkdir(base_path + "/templates")
    trymkdir(base_path + "/templates/" + modulename)
    view_content = """
import os
import json

from flask import Blueprint
# from flask import render_template
# from flask import url_for
# from flask import redirect
# from flask import flash
# from flask import request

# # 
# from shopyoapi.html import notify_success
# from shopyoapi.forms import flash_errors

dirpath = os.path.dirname(os.path.abspath(__file__))
module_info = {}

with open(dirpath + "/info.json") as f:
    module_info = json.load(f)

globals()['{}_blueprint'.format(module_info["module_name"])] = Blueprint(
    "{}".format(module_info["module_name"]),
    __name__,
    template_folder="templates",
    url_prefix=module_info["url_prefix"],
)


module_blueprint = globals()['{}_blueprint'.format(module_info["module_name"])]

@module_blueprint.route("/")
def index():
    return module_info['display_string']
"""
    trymkfile(base_path + "/" + "view.py", view_content)
    trymkfile(base_path + "/" + "forms.py", "")
    trymkfile(base_path + "/" + "models.py", "")
    info_json_content = """{{
        "display_string": "{0}",
        "module_name":"{1}",
        "type": "show",
        "fa-icon": "fa fa-store",
        "url_prefix": "/{1}",
        "author": {{
            "name":"",
            "website":"",
            "mail":""
        }}
}}""".format(
        modulename.capitalize(), modulename
    )
    trymkfile(base_path + "/" + "info.json", info_json_content)

    trymkdir(base_path + "/templates/" + modulename + "/blocks")
    trymkfile(
        base_path + "/templates/" + modulename + "/blocks/" + "sidebar.html",
        "",
    )
