'''
commandline utilities functions


# Past view.py code

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
'''

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
    subprocess.run(
        [sys.executable, "manage.py", "db", "init"], stdout=subprocess.PIPE
    )

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


def create_module(modulename, base_path=None):
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
    if not base_path:
        base_path = "modules/" + modulename
    trymkdir(base_path)
    trymkdir(base_path + "/templates")
    trymkdir(base_path + "/templates/" + modulename)
    trymkdir(base_path + "/tests")
    test_func_content = """
Please add your functional tests to this file.
"""
    test_model_content = """
Please add your models tests to this file.
"""
    trymkfile(base_path + "/tests/" + "test_"+ modulename + "_functional.py", test_func_content)
    trymkfile(base_path + "/tests/" + "test_"+ modulename + "_models.py", test_model_content)
    view_content = """
from shopyoapi.module import ModuleHelp
# from flask import render_template
# from flask import url_for
# from flask import redirect
# from flask import flash
# from flask import request

# from shopyoapi.html import notify_success
# from shopyoapi.forms import flash_errors

mhelp = ModuleHelp(__file__, __name__)
globals()[mhelp.blueprint_str] = mhelp.blueprint
module_blueprint = globals()[mhelp.blueprint_str]

@module_blueprint.route("/")
def index():
    return mhelp.info['display_string']

# If "dashboard": "/dashboard" is set in info.json
# 
# @module_blueprint.route("/dashboard", methods=["GET"])
# def dashboard():

#     context = mhelp.context()

#     context.update({

#         })
#     return mhelp.render('dashboard.html', **context)
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
    dashboard_file_content = '''
{% extends "base/module_base.html" %}
{% set active_page = info['display_string']+' dashboard' %}
{% block pagehead %}
<title></title>
<style>
</style>
{% endblock %}
{% block sidebar %}
{% include info['module_name']+'/blocks/sidebar.html' %}
{% endblock %}
{% block content %}
<br>

<div class="card">
    <div class="card-body">

    </div>
 </div>
{% endblock %}
'''
    trymkfile(
        os.path.join(base_path, "templates", modulename, 'dashboard.html'),
        dashboard_file_content
    )

    global_file_content = """
available_everywhere = {
    
}
"""
    trymkfile(
        os.path.join(base_path, "global.py"), global_file_content,
    )


def create_box(name):
    """
    creates box with box_info.json

    Parameters
    ----------
    name: str
        name of box, in alphanumeric-underscore

    Returns
    -------
    None


    """
    base_path = "modules/" + "box__" + name
    if os.path.exists(base_path):
        print("Box {} exists!".format(base_path))
    else:
        trymkdir(base_path)
        info_json_content = """{{
        "display_string": "{0}",
        "box_name":"{1}",
        "author": {{
            "name":"",
            "website":"",
            "mail":""
        }}
    }}""".format(
            name.capitalize(), name
        )
        trymkfile(base_path + "/" + "box_info.json", info_json_content)


def create_module_in_box(modulename, boxname):
    """
    creates module with the structure defined in the modules section in docs in
    a box

    Parameters
    ----------
    modulename: str
        name of module, in alphanumeric-underscore

    boxname: str
        name of box, in alphanumeric-underscore

    Returns
    -------
    None


    """
    box_path = os.path.join("modules", boxname)
    module_path = os.path.join("modules", boxname, modulename)

    if not boxname.startswith("box__"):
        print("Invalid box {}. Boxes should start with box__".format(boxname))

    elif not os.path.exists(box_path):
        print("Box {} does not exists!".format(box_path))
        available_boxes = "\n* ".join(
            [f for f in os.listdir("modules/") if f.startswith("box__")]
        )
        print("Available boxes: \n* {}".format(available_boxes))

    elif os.path.exists(module_path):
        print("Module {} exists".format(module_path))

    else:
        print("Creating module {}".format(module_path))
        create_module(modulename, base_path=module_path)
