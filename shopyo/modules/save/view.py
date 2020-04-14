import os
import json

from flask import Blueprint, render_template, request, redirect
from flask_login import login_required, current_user

from shopyoapi.init import db, login_manager
from modules.appointment.models import Appointments
from project_api import base_context

import requests

dirpath = os.path.dirname(os.path.abspath(__file__))
module_info = {}

with open(dirpath + "/info.json") as f:
    module_info = json.load(f)

save_blueprint = Blueprint(
    "save", __name__, template_folder="templates", url_prefix=module_info["url_prefix"]
)


@save_blueprint.route("/")
@login_required
def save_main():
    context = base_context()

    def has_internet():
        url = "http://www.google.com/"
        timeout = 5
        try:
            _ = requests.get(url, timeout=timeout)
            return True
        except requests.ConnectionError:
            pass
        return False

    context["has_internet"] = has_internet()
    return render_template("save/index.html", **context)


@save_blueprint.route("/upload")
@login_required
def upload_db():
    context = base_context()

    def has_internet():
        url = "http://www.google.com/"
        timeout = 5
        try:
            _ = requests.get(url, timeout=timeout)
            return True
        except requests.ConnectionError:
            pass
        return False

    context["has_internet"] = has_internet()
    return render_template("save/index.html", **context)
