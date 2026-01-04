import json
import os

from flask import current_app
from flask import flash
from flask import render_template
from flask_login import login_required
from modules.box__default.appadmin.admin import admin_required
from modules.box__default.auth.decorators import check_confirmed
from modules.box__default.theme.helpers import get_active_back_theme
from shopyo.api.html import notify_success
from shopyo.api.module import ModuleHelp

mhelp = ModuleHelp(__file__, __name__)
globals()[mhelp.blueprint_str] = mhelp.blueprint
module_blueprint = globals()[mhelp.blueprint_str]


all_info = {}


@module_blueprint.route("/")
@login_required
@check_confirmed
@admin_required
def index():
    return render_template(f"{get_active_back_theme()}/index.html")
