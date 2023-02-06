from flask import redirect
from flask import request
from flask import session
from modules.box__default.i18n.helpers import lang_keys
from shopyo.api.module import ModuleHelp
from shopyo.api.security import get_safe_redirect

# from flask import render_template
# from flask import url_for
# from flask import redirect
# from flask import flash
# from flask import request

# from shopyo.api.html import notify_success
# from shopyo.api.forms import flash_errors

mhelp = ModuleHelp(__file__, __name__)
globals()[mhelp.blueprint_str] = mhelp.blueprint
module_blueprint = globals()[mhelp.blueprint_str]


@module_blueprint.route("/")
def index():
    return mhelp.info["display_string"]


@module_blueprint.route("/set-lang", methods=["GET"])
def set_lang():
    set_to_lang = request.args.get("lang", "en")
    next_url = request.args.get("next", "/")

    if set_to_lang in lang_keys():
        session["yo_current_lang"] = set_to_lang
        session["yo_default_lang"] = set_to_lang

        return redirect(get_safe_redirect(next_url))


# If "dashboard": "/dashboard" is set in info.json
#
# @module_blueprint.route("/dashboard", methods=["GET"])
# def dashboard():

#     context = mhelp.context()

#     context.update({

#         })
#     return mhelp.render('dashboard.html', **context)
