import os
import json

from flask import Blueprint
from flask import render_template
from flask_login import login_required

from shopyoapi.enhance import base_context


control_panel_blueprint = Blueprint(
    "control_panel",
    __name__,
    template_folder="templates",
    url_prefix="/control_panel",
)
all_info = {}

base_path = os.path.dirname(os.path.abspath(__file__))

@control_panel_blueprint.route("/")
@login_required
def index():
    context = base_context()

    for module in os.listdir(os.path.join(base_path, "modules")):
        if module.startswith("__"):
            continue
        if module not in ["control_panel"]:
            file_path = "modules/{}/info.json".format(module)
            with open(os.path.join(base_path, file_path)) as f:
                module_info = json.load(f)
                all_info[module] = module_info

    context["all_info"] = all_info
    return render_template("control_panel/index.html", **context)
