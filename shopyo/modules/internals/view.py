import os
import json

from flask import Blueprint
from flask import render_template
from flask_login import login_required

from shopyoapi.enhance import base_context

internals_blueprint = Blueprint(
    "internals",
    __name__,
    url_prefix='/internals',
    template_folder="templates",
)
all_info = {}

@internals_blueprint.route("/")
@login_required
def index():
    context = base_context()

    for module in os.listdir("modules"):
        if module.startswith("__"):
            continue
        if module not in ["control_panel"]:
            with open("modules/{}/info.json".format(module)) as f:
                module_info = json.load(f)
                all_info[module] = module_info

    context["all_info"] = all_info
    return render_template("internals/index.html", **context)
