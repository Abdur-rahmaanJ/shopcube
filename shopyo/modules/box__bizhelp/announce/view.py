

# from flask import render_template
# from flask import url_for
# from flask import redirect
# from flask import flash
# from flask import request

# from shopyoapi.html import notify_success
# from shopyoapi.forms import flash_errors
from shopyoapi.module import ModuleHelp

from .forms import AnnounceForm

from flask_login import login_required

mhelp = ModuleHelp(__file__, __name__)
globals()[mhelp.blueprint_str] = mhelp.blueprint
module_blueprint = globals()[mhelp.blueprint_str]

@module_blueprint.route("/")
def index():
    return mhelp.info['display_string']


# TODO add pagination
@module_blueprint.route("/dashboard", methods=["GET"])
@login_required
def dashboard():

    context = mhelp.context()
    form = AnnounceForm()
    context.update({
        'form': form
        })
    return mhelp.render('dashboard.html', **context)


@module_blueprint.route("/add/check", methods=["GET", "POST"])
@login_required
def add_check():
    return ''