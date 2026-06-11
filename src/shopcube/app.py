"""
Temporary notice:

Need help?

- Join the discord https://discord.com/invite/k37Ef6w
- Raise an issue https://github.com/shopyo/shopyo/issues/new/choose
- Mail maintainers https://github.com/shopyo/shopyo#-contact

Hope it helps! We welcome all questions and even requests for walkthroughs
"""
import importlib
import json
import os
import sys
import warnings
warnings.filterwarnings("ignore", message=".*pkg_resources.*deprecated.*")
warnings.filterwarnings("ignore", message=".*Using the in-memory storage.*")

import jinja2
from flask import Flask
from flask_admin import Admin
from flask_admin.menu import MenuLink
from flask_login import current_user
from shopyo.api.assets import get_static
from shopyo.api.assets import register_devstatic
from shopyo.api.debug import is_yo_debug
from shopyo.api.file import trycopy
base_path = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, base_path)
from config import app_config

# from init import db
from init import load_extensions
from init import modules_path
from init import installed_packages
from init import configure_all_uploads


from shopyo_admin import MyAdminIndexView
from shopyo_auth import ShopyoAuth
from shopyo_base import ShopyoBase
from shopyo_dashboard import ShopyoDashboard
from shopyo_theme import ShopyoTheme
from shopyo_theme import (
    get_active_front_theme,
    get_active_front_theme_version,
    get_active_front_theme_styles_url,
    get_active_back_theme,
    get_active_back_theme_version,
    get_active_back_theme_styles_url,
)
from shopyo_appadmin import ShopyoAppAdmin
from shopyo_page import ShopyoPage
from shopyo_settings import ShopyoSettings
from shopyo_settings.helpers import get_setting, set_setting


def create_app(config_name="development", instance_path=None):

    global_template_variables = {}
    global_configs = {}
    
    if instance_path is None:
        # Default to 'instance' in current working directory for deployments
        instance_path = os.path.join(os.getcwd(), "instance")
    
    app = Flask(
        __name__,
        instance_path=instance_path,
        instance_relative_config=True,
    )

    load_plugins(app, global_template_variables, global_configs, config_name)
    load_config_from_obj(app, config_name)
    load_config_from_instance(app, config_name)
    create_config_json()
    load_extensions(app)
    shopyo_base = ShopyoBase(app)
    shopyo_dashboard = ShopyoDashboard(app)
    shopyo_auth = ShopyoAuth(app)
    shopyo_theme = ShopyoTheme(app)
    shopyo_appadmin = ShopyoAppAdmin(app)
    shopyo_page = ShopyoPage(app)
    shopyo_settings = ShopyoSettings(app)
    setup_flask_admin(app)
    register_devstatic(app, modules_path)
    load_blueprints(app, config_name, global_template_variables, global_configs)
    setup_theme_paths(app)
    inject_global_vars(app, global_template_variables)
    configure_all_uploads(app)
    return app


def load_plugins(app, global_template_variables, global_configs, config_name):
    for plugin in installed_packages:
        if plugin not in ["shopyo_admin"]:
            try:
                mod = importlib.import_module(f"{plugin}.view")
                app.register_blueprint(getattr(mod, f"{plugin}_blueprint"))
            except AttributeError:
                # print("[ ] Blueprint skipped:", e)
                pass

            # global's available everywhere template vars
            try:
                mod_global = importlib.import_module(f"{plugin}.global")
                global_template_variables.update(mod_global.available_everywhere)
            except ImportError as e:
                if is_yo_debug():
                    print("[ ] Not loading template variable", e)

            except AttributeError as e:
                if is_yo_debug():
                    print("[ ] Not loading template variable", e)

            # load configs
            try:
                mod_global = importlib.import_module(f"{plugin}.global")
                if config_name in mod_global.configs:
                    global_configs.update(mod_global.configs.get(config_name))
            except ImportError as e:
                # print(f"[ ] {e}")
                if is_yo_debug():
                    print("[ ] Not loading template variable", e)
            except AttributeError as e:
                # click.echo('info: config not found in global')
                if is_yo_debug():
                    print("[ ] Not loading template variable", e)


def load_config_from_obj(app, config_name):

    try:
        configuration = app_config[config_name]
    except KeyError as e:
        print(
            f"[ ] Invalid config name {e}. Available configurations are: "
            f"{list(app_config.keys())}\n"
        )
        sys.exit(1)

    app.config.from_object(configuration)


def load_config_from_instance(app, config_name):

    if config_name != "testing":
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile("config.py", silent=True)

    # create empty instance folder and empty config if not present
    try:
        os.makedirs(app.instance_path)
        with open(os.path.join(app.instance_path, "config.py"), "a"):
            pass
    except OSError:
        pass


def create_config_json():
    if not os.path.exists("config.json"):
        config_src = os.path.join(base_path, "config_demo.json")
        config_dst = os.path.join(os.getcwd(), "config.json")
        if os.path.exists(config_src):
            trycopy(config_src, config_dst)


def setup_flask_admin(app):
    admin = Admin(
        app,
        name="My App",
        template_mode="bootstrap4",
        index_view=MyAdminIndexView(),
    )
    # admin.add_view(DefaultModelView(Settings, db.session))
    admin.add_link(MenuLink(name="Logout", category="", endpoint="shopyo_auth.logout"))


def load_blueprints(app, config_name, global_template_variables, global_configs):
    """
    - Registers blueprints
    - Adds global template objects from modules
    - Adds global configs from modules
    """
    for folder in os.listdir(os.path.join(base_path, "modules")):
        if folder.startswith("__"):  # ignore __pycache__
            continue

        if folder.startswith("box__"):
            # boxes
            for sub_folder in os.listdir(os.path.join(base_path, "modules", folder)):
                if sub_folder.startswith("__"):  # ignore __pycache__
                    continue
                elif sub_folder.endswith(".json"):  # box_info.json
                    continue
                elif sub_folder == "dashboard":  # old dashboard replaced by shopyo_dashboard
                    continue
                try:
                    sys_mod = importlib.import_module(
                        f"modules.{folder}.{sub_folder}.view"
                    )
                    app.register_blueprint(getattr(sys_mod, f"{sub_folder}_blueprint"))
                except (AttributeError, ModuleNotFoundError):
                    pass
                try:
                    mod_global = importlib.import_module(
                        f"modules.{folder}.{sub_folder}.global"
                    )
                    global_template_variables.update(mod_global.available_everywhere)
                except (ImportError, AttributeError) as e:
                    if is_yo_debug():
                        print("[ ] skipped", e)

                except AttributeError as e:
                    if is_yo_debug():
                        print("[ ] skipped", e)

                # load configs
                try:
                    mod_global = importlib.import_module(
                        f"modules.{folder}.{sub_folder}.global"
                    )
                    if config_name in mod_global.configs:
                        global_configs.update(mod_global.configs.get(config_name))
                except ImportError as e:
                    if is_yo_debug():
                        print("[ ] skipped", e)

                except AttributeError as e:
                    # click.echo('info: config not found in global')
                    if is_yo_debug():
                        print("[ ] skipped", e)
        else:
            # apps
            try:
                mod = importlib.import_module(f"modules.{folder}.view")
                app.register_blueprint(getattr(mod, f"{folder}_blueprint"))
            except AttributeError as e:
                if is_yo_debug():
                    print("[ ] skipped", e)

            # global's available everywhere template vars
            try:
                mod_global = importlib.import_module(f"modules.{folder}.global")
                global_template_variables.update(mod_global.available_everywhere)
            except ImportError as e:
                # print(f"[ ] {e}")
                if is_yo_debug():
                    print("[ ] skipped", e)

            except AttributeError as e:
                if is_yo_debug():
                    print("[ ] skipped", e)

            # load configs
            try:
                mod_global = importlib.import_module(f"modules.{folder}.global")
                if config_name in mod_global.configs:
                    global_configs.update(mod_global.configs.get(config_name))
            except ImportError as e:
                # print(f"[ ] {e}")
                if is_yo_debug():
                    print("[ ] skipped", e)
            except AttributeError as e:
                # click.echo('info: config not found in global')
                if is_yo_debug():
                    print("[ ] skipped", e)

    app.config.update(**global_configs)


def setup_theme_paths(app):
    with app.app_context():
        front_theme_dir = os.path.join(
            app.config["BASE_DIR"], "static", "themes", "front"
        )
        back_theme_dir = os.path.join(
            app.config["BASE_DIR"], "static", "themes", "back"
        )

        if os.path.exists(front_theme_dir) and os.path.exists(back_theme_dir):
            my_loader = jinja2.ChoiceLoader(
                [
                    app.jinja_loader,
                    jinja2.FileSystemLoader([front_theme_dir, back_theme_dir]),
                ]
            )
            app.jinja_loader = my_loader


def get_modules_info():
    all_info = {}
    modules_dir = os.path.join(base_path, "modules")
    if not os.path.exists(modules_dir):
        return all_info
    for folder in os.listdir(modules_dir):
        if folder.startswith("__"):
            continue
        elif folder.startswith("box__"):
            for sub_folder in os.listdir(os.path.join(modules_dir, folder)):
                if sub_folder.startswith("__") or sub_folder.endswith(".json"):
                    continue
                info_path = os.path.join(modules_dir, folder, sub_folder, "info.json")
                if os.path.exists(info_path):
                    with open(info_path) as f:
                        module_info = json.load(f)
                    if "fa-icon" not in module_info and "icons" in module_info:
                        module_info["fa-icon"] = module_info["icons"].get("fa", "")
                    module_info["static_name"] = f"{folder}/{sub_folder}"
                    all_info[sub_folder] = module_info
        else:
            info_path = os.path.join(modules_dir, folder, "info.json")
            if os.path.exists(info_path):
                with open(info_path) as f:
                    module_info = json.load(f)
                if "fa-icon" not in module_info and "icons" in module_info:
                    module_info["fa-icon"] = module_info["icons"].get("fa", "")
                module_info["static_name"] = folder
                all_info[folder] = module_info
    return all_info


def get_url_prefix(parts=False, as_str=False):
    from flask import request
    if parts:
        if as_str:
            return str(request.url_rule)
        else:
            return str(request.url_rule).split("/")
    else:
        return "/" + str(request.url_rule).split("/")[1]


def inject_global_vars(app, global_template_variables):
    @app.context_processor
    def inject_global_vars():
        APP_NAME = "dwdwefw"

        base_context = {
            "APP_NAME": APP_NAME,
            "len": len,
            "current_user": current_user,
            "get_static": get_static,
            "get_modules_info": get_modules_info,
            "get_url_prefix": get_url_prefix,
            "get_active_front_theme": get_active_front_theme,
            "get_active_front_theme_version": get_active_front_theme_version,
            "get_active_front_theme_styles_url": get_active_front_theme_styles_url,
            "get_active_back_theme": get_active_back_theme,
            "get_active_back_theme_version": get_active_back_theme_version,
            "get_active_back_theme_styles_url": get_active_back_theme_styles_url,
            "get_setting": get_setting,
            "set_setting": set_setting,
        }
        base_context.update(global_template_variables)

        return base_context
