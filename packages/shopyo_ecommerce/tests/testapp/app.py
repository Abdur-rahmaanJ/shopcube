"""
Temporary notice:

Need help?

- Join the discord https://discord.com/invite/k37Ef6w
- Raise an issue https://github.com/shopyo/shopyo/issues/new/choose
- Mail maintainers https://github.com/shopyo/shopyo#-contact

Hope it helps! We welcome all questions and even requests for walkthroughs
"""

import importlib
import os
import sys

import click
import jinja2
from flask import Flask
from flask_admin import Admin
from flask_admin.menu import MenuLink
from flask_login import current_user

from shopyo.api.assets import get_static
from shopyo.api.assets import register_shopyo_static
from shopyo.api.debug import is_yo_debug
from shopyo.api.file import trycopy
from shopyo_ecommerce import ShopyoEcommerce


base_path = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, base_path)
from config import app_config

# from init import db
from init import load_extensions
from init import modules_path

try:
    from init import installed_packages
except ImportError:
    click.echo(
        "This version of Shopyo requires that\n"
        "init.py contains the line\n"
        "installed_packages = []\n"
        "please add it."
    )
    sys.exit()

from shopyo_admin import MyAdminIndexView


def create_app(config_name="development"):
    global_template_variables = {}
    global_configs = {}
    app = Flask(
        __name__,
        instance_path=os.path.join(base_path, "instance"),
        instance_relative_config=True,
    )

    load_plugins(app, global_template_variables, global_configs, config_name)
    load_config_from_obj(app, config_name)
    load_config_from_instance(app, config_name)
    load_extensions(app)
    ShopyoEcommerce(app)

    setup_flask_admin(app)
    register_shopyo_static(app, modules_path)
    load_blueprints(app, config_name, global_template_variables, global_configs)
    setup_theme_paths(app)
    inject_global_vars(app, global_template_variables)
    from init import db

    custom_commands(db, app)
    return app


def _register_module(
    app, module_name, global_template_variables, global_configs, config_name
):
    """
    Helper to register a module/plugin:
    1. Register blueprint from .view
    2. Update global_template_variables from .global
    3. Update global_configs from .global
    """

    try:
        view_mod = importlib.import_module(f"{module_name}.view")
        # Try 'blueprint' attribute first
        bp = getattr(view_mod, "blueprint", None)
        if bp is None:
            # Fallback: try 'modulename_blueprint'
            # For modules.box__x.mod_y -> mod_y
            short_name = module_name.split(".")[-1]
            bp = getattr(view_mod, f"{short_name}_blueprint", None)

        if bp:
            app.register_blueprint(bp)
    except (ImportError, AttributeError) as e:
        if isinstance(e, AttributeError):
            if is_yo_debug():
                print(f"[ ] Blueprint skipped for {module_name}: {e}")
        else:
            raise e

    try:
        global_mod = importlib.import_module(f"{module_name}.global")
        if hasattr(global_mod, "available_everywhere"):
            global_template_variables.update(global_mod.available_everywhere)
    except (ImportError, AttributeError) as e:
        if is_yo_debug():
            print(f"[ ] Template var skipped for {module_name}: {e}")

    try:
        global_mod = importlib.import_module(f"{module_name}.global")
        if hasattr(global_mod, "configs") and config_name in global_mod.configs:
            global_configs.update(global_mod.configs[config_name])
    except (ImportError, AttributeError) as e:
        if is_yo_debug():
            print(f"[ ] Config skipped for {module_name}: {e}")


def load_plugins(app, global_template_variables, global_configs, config_name):
    for plugin in installed_packages:
        if plugin not in ["shopyo_admin"]:
            _register_module(
                app, plugin, global_template_variables, global_configs, config_name
            )


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


def setup_flask_admin(app):
    admin = Admin(
        app,
        name="My App",
        index_view=MyAdminIndexView(),
    )
    # admin.add_view(DefaultModelView(Settings, db.session))
    admin.add_link(MenuLink(name="Logout", category="", url="/auth/logout?next=/admin"))


def load_blueprints(app, config_name, global_template_variables, global_configs):
    """
    - Registers blueprints
    - Adds global template objects from modules
    - Adds global configs from modules
    """
    from shopyo.api.module import iter_modules

    for module_name, _ in iter_modules(base_path):
        _register_module(
            app, module_name, global_template_variables, global_configs, config_name
        )

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


def inject_global_vars(app, global_template_variables):
    @app.context_processor
    def inject_global_vars():
        base_context = {
            "APP_NAME": "My App",
            "OUR_APP_NAME": "My App",
            "len": len,
            "current_user": current_user,
            "get_static": get_static,
        }
        base_context.update(global_template_variables)

        return base_context


def custom_commands(db, app):
    from flask.cli import with_appcontext

    @click.command("shopyo-seed")
    @with_appcontext
    def shopyo_upload():

        for ext in app.extensions:
            if ext.startswith("shopyo_"):
                try:
                    e = app.extensions[ext]
                    e.upload()
                    db.session.commit()
                    click.echo("Uploaded for " + ext)
                except AttributeError as e:
                    pass

    app.cli.add_command(shopyo_upload)
