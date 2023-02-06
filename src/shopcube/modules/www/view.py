from flask import render_template
from modules.box__default.theme.helpers import get_active_front_theme
from shopyo.api.module import ModuleHelp
from shopyo.api.templates import yo_render

# from flask import url_for
# from flask import redirect
# from flask import flash
# from flask import request
#
# from shopyo.api.html import notify_success
# from shopyo.api.forms import flash_errors
# from shopyo.api.enhance import get_active_theme_dir
# from shopyo.api.enhance import get_setting
# from modules.box__ecommerce.shop.helpers import get_cart_data

mhelp = ModuleHelp(__file__, __name__)
globals()[mhelp.blueprint_str] = mhelp.blueprint
module_blueprint = globals()[mhelp.blueprint_str]


@module_blueprint.route("/")
def index():
    # cant be defined above but must be manually set each time
    # active_theme_dir = os.path.join(
    #     dirpath, "..", "..", "themes", get_setting("ACTIVE_FRONT_THEME")
    # )
    # module_blueprint.template_folder = active_theme_dir

    # return str(module_blueprint.template_folder)

    # return render_template(get_setting("ACTIVE_FRONT_THEME") + "/index.html")

    return render_template(
        f"{get_active_front_theme()}/index.html", get_static=get_static
    )


from shopyo.api.assets import get_static


@module_blueprint.route("/render_demo")
def render_demo():
    context = {"fruit": "mango"}
    return yo_render("blogus/render_demo.html", context)
