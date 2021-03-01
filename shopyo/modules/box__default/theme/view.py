import json
import os

from flask import Blueprint
from flask import current_app
from flask import redirect
from flask import render_template
from flask import url_for

from flask_login import login_required

from modules.box__default.settings.helpers import get_setting
from shopyo.api.enhance import set_setting
from shopyo.api.file import get_folders

# from flask import flash
# from flask import request
# from shopyo.api.html import notify_success
# from init import db

# from modules.box__default.settings.models import Settings

# from shopyo.api.forms import flash_errors


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

    context = {}

    front_themes_path = os.path.join(
        current_app.config["BASE_DIR"], "static", "themes", "front"
    )
    all_front_info = {}
    front_theme_folders = get_folders(front_themes_path)
    for folder in front_theme_folders:
        theme_path = os.path.join(front_themes_path, folder)
        info_path = os.path.join(theme_path, "info.json")
        with open(info_path) as f:
            all_front_info[folder] = json.load(f)

    back_themes_path = os.path.join(
        current_app.config["BASE_DIR"], "static", "themes", "back"
    )
    all_back_info = {}
    back_theme_folders = get_folders(back_themes_path)
    for folder in back_theme_folders:
        theme_path = os.path.join(back_themes_path, folder)
        info_path = os.path.join(theme_path, "info.json")
        with open(info_path) as f:
            all_back_info[folder] = json.load(f)

    active_front_theme = get_setting("ACTIVE_FRONT_THEME")
    active_back_theme = get_setting("ACTIVE_BACK_THEME")

    context.update(
        {
            "all_front_info": all_front_info,
            "all_back_info": all_back_info,
            "active_front_theme": active_front_theme,
            "active_back_theme": active_back_theme,
        }
    )
    context.update(module_settings)

    return render_template(
        "{}/index.html".format(module_info["module_name"]), **context
    )


@module_blueprint.route("/activate/front/<theme_name>")
@login_required
def activate_front_theme(theme_name):
    set_setting("ACTIVE_FRONT_THEME", theme_name)

    # with app.app_context():

    # current_app.jinja_loader,
    # print(current_app.jinja_loader.list_templates())
    return redirect(url_for("{}.index".format(module_info["module_name"])))


@module_blueprint.route("/activate/back/<theme_name>")
@login_required
def activate_back_theme(theme_name):
    set_setting("ACTIVE_BACK_THEME", theme_name)

    # with app.app_context():

    # current_app.jinja_loader,
    # print(current_app.jinja_loader.list_templates())
    return redirect(url_for("{}.index".format(module_info["module_name"])))
