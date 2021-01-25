import json
import os

# from flask import url_for
# from flask import redirect
# from flask import flash
# from flask import request
from flask import Blueprint
from flask import current_app
from flask import redirect
from flask import render_template
from flask import url_for

#
# from shopyoapi.html import notify_success
# from shopyoapi.forms import flash_errors
# from shopyoapi.enhance import get_active_theme_dir
# from shopyoapi.enhance import get_setting

# from modules.box__ecommerce.shop.helpers import get_cart_data

dirpath = os.path.dirname(os.path.abspath(__file__))
module_info = {}

with open(dirpath + "/info.json") as f:
    module_info = json.load(f)


globals()["{}_blueprint".format(module_info["module_name"])] = Blueprint(
    "{}".format(module_info["module_name"]),
    __name__,
    template_folder="",
    url_prefix=module_info["url_prefix"],
)


module_blueprint = globals()["{}_blueprint".format(module_info["module_name"])]


@module_blueprint.route("/")
def index():
    # cant be defined above but must be manually set each time
    # active_theme_dir = os.path.join(
    #     dirpath, "..", "..", "themes", get_setting("ACTIVE_FRONT_THEME")
    # )
    # module_blueprint.template_folder = active_theme_dir

    # return str(module_blueprint.template_folder)

    return redirect(url_for("shop.homepage"))
