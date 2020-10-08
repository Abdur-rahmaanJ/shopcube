import os
import json

from flask import Blueprint
from flask import render_template
from flask import request

from shopyoapi.enhance import base_context
from shopyoapi.forms import flash_errors

from .forms import PageForm

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


module_blueprint = globals()["{}_blueprint".format(module_info["module_name"])]

module_name = module_info["module_name"]


@module_blueprint.route("/")
def index():
    return ""


@module_blueprint.route(module_info["panel_redirect"])
def panel_redirect():
    context = base_context()
    form = PageForm()

    context.update({"form": form, "module_name": module_name})
    return render_template("page/dashboard.html", **context)


@module_blueprint.route("/check_pagecontent", methods=["GET", "POST"])
def check_pagecontent():
    if request.method == "POST":
        form = PageForm()
        if not form.validate_on_submit():
            flash_errors(form)
            return redirect(url_for("{}.panel_redirect".format(module_name)))

        return form.content.data
