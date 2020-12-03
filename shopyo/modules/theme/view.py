import json
import os

from flask import Blueprint
from flask import current_app
from flask import redirect
from flask import render_template
from flask import url_for

from flask_login import login_required

from shopyoapi.enhance import base_context
from shopyoapi.enhance import get_setting
from shopyoapi.enhance import set_setting
from shopyoapi.file import get_folders
from shopyoapi.init import db

from modules.settings.models import Settings

# from flask import flash
# from flask import request


# from shopyoapi.html import notify_success
# from shopyoapi.forms import flash_errors


dirpath = os.path.dirname(os.path.abspath(__file__))
module_info = {}

with open(dirpath + "/info.json") as f:
    module_info = json.load(f)

globals()["{}_blueprint".format(module_info["module_name"])] = Blueprint(
    "{}".format(module_info["module_name"]),
    __name__,
    template_folder="templates",
    url_prefix=module_info["url_prefix"],
)

module_settings = {"module_info": module_info}

module_blueprint = globals()["{}_blueprint".format(module_info["module_name"])]


@module_blueprint.route("/")
@login_required
def index():

    context = base_context()
    themes_path = os.path.join(current_app.config["BASE_DIR"], "themes")
    all_info = {}
    theme_folders = get_folders(themes_path)
    for folder in theme_folders:
        theme_path = os.path.join(themes_path, folder)
        info_path = os.path.join(theme_path, "info.json")
        with open(info_path) as f:
            all_info[folder] = json.load(f)

    active_theme = get_setting("ACTIVE_THEME")
    context.update({"all_info": all_info, "active_theme": active_theme})
    context.update(module_settings)
    return render_template(
        "{}/index.html".format(module_info["module_name"]), **context
    )


@module_blueprint.route("/activate/<theme_name>")
@login_required
def activate(theme_name):
    set_setting("ACTIVE_THEME", theme_name)
    return redirect(url_for("{}.index".format(module_info["module_name"])))
