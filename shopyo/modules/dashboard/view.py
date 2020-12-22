import json
import os

from flask import Blueprint
from flask import current_app
from flask import flash
from flask import render_template

from flask_login import login_required

from shopyoapi.html import notify_success

dashboard_blueprint = Blueprint(
    "dashboard",
    __name__,
    template_folder="templates",
    url_prefix="/dashboard",
)
all_info = {}


@dashboard_blueprint.route("/")
@login_required
def index():
    context = {}

    for module in os.listdir(os.path.join(current_app.config["BASE_DIR"], "modules")):
        if module.startswith("__"):
            continue
        if module not in ["dashboard"]:
            with open(
                os.path.join(
                    current_app.config["BASE_DIR"],
                    "modules",
                    module,
                    "info.json",
                )
            ) as f:
                module_info = json.load(f)
                all_info[module] = module_info

    context["all_info"] = all_info
    flash(notify_success("Notif test"))
    return render_template("dashboard/index.html", **context)
