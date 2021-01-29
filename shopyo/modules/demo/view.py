
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
    return '<img src="{}">'.format(mhelp.get_module_asset('demo/Desert.jpg'))

# If "dashboard": "/dashboard" is set in info.json
#
# @module_blueprint.route("/dashboard", methods=["GET"])
# def dashboard():

#     context = mhelp.context()

#     context.update({

#         })
#     return mhelp.render('dashboard.html', **context)
