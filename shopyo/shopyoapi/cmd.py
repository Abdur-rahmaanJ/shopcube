"""
commandline utilities functions
"""
import json
import os
import re
import subprocess
import sys

from app import app
from shopyoapi.init import db
from shopyoapi.uploads import add_admin
from shopyoapi.uploads import add_setting
from shopyoapi.uploads import add_uncategorised_category
from shopyoapi.cmd_helper import remove_pycache
from shopyoapi.cmd_helper import remove_file_or_dir
from .file import trymkdir
from .file import trymkfile


def clean():
    """
    Deletes shopyo.db and migrations/ if present in current working directory.
    Deletes all __pycache__ folders starting from current working directory
    all the way to leaf directory.

    Parameters
    ----------


    Returns
    -------
    None
        ...

    """
    # getting app context creates the shopyo.db file even if it is not present
    with app.test_request_context():
        db.drop_all()
        db.engine.execute('DROP TABLE IF EXISTS alembic_version;')
        print("[x] all tables dropped")

    remove_pycache(os.getcwd())
    remove_file_or_dir("shopyo.db")
    remove_file_or_dir("migrations")


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
            "Error: modulename is not valid, please use alphanumeric\
             and underscore only"
        )
        sys.exit()
    print(f"creating module: {modulename}")
    if not base_path:
        base_path = f"modules/{modulename}"
    trymkdir(base_path)
    trymkdir(f"{base_path}/templates")
    trymkdir(f"{base_path}/templates/{modulename}")
    trymkdir(f"{base_path}/tests")
    test_func_content = """
Please add your functional tests to this file.
"""
    test_model_content = """
Please add your models tests to this file.
"""
    trymkfile(
        f"{base_path}/tests/test_{modulename}_functional.py",
        test_func_content
    )
    trymkfile(
        f"{base_path}/tests/test_{modulename}_models.py",
        test_model_content
    )
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
    trymkfile(f"{base_path}/view.py", view_content)
    trymkfile(f"{base_path}/forms.py", "")
    trymkfile(f"{base_path}/models.py", "")
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
    trymkfile(f"{base_path}/info.json", info_json_content)

    trymkdir(f"{base_path}/templates/{modulename}/blocks")
    trymkfile(f"{base_path}/templates/{modulename}/blocks/sidebar.html", "")
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
        f"{base_path}/templates/{modulename}/dashboard.html",
        dashboard_file_content
    )
    global_file_content = """
available_everywhere = {

}
"""
    trymkfile(f"{base_path}/global.py", global_file_content)


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
    base_path = f"modules/box__{name}"
    if os.path.exists(base_path):
        print(f"Box {base_path} exists!")
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
        trymkfile(f"{base_path}/box_info.json", info_json_content)


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
        print(f"Invalid box {boxname}. Boxes should start with box__")

    elif not os.path.exists(box_path):
        print(f"Box {box_path} does not exists!")
        available_boxes = "\n* ".join(
            [f for f in os.listdir("modules/") if f.startswith("box__")]
        )
        print(f"Available boxes: \n* {available_boxes}")

    elif os.path.exists(module_path):
        print(f"Module {module_path} exists")

    else:
        print(f"Creating module {module_path}")
        create_module(modulename, base_path=module_path)
