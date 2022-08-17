import importlib
import os
import json
import sys

from flask import Flask

# from flask import redirect
from flask import url_for
from flask import send_from_directory
import logging
from flask_login import current_user
from flask_wtf.csrf import CSRFProtect

sys.path.append(".")

import jinja2
from flask_uploads import configure_uploads
from flask_mailman import Mail


from init import categoryphotos
from init import db
from init import login_manager
from init import ma
from init import migrate
from init import productphotos
from init import subcategoryphotos
from init import modules_path
from shopyo.api.file import trycopy


from config import app_config

logging.basicConfig(level=logging.DEBUG)

base_path = os.path.dirname(os.path.abspath(__file__))

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

def create_app(config_name, configs=None):

    app = Flask(__name__)

    load_config_from_obj(app, config_name)
    load_config_from_instance(app, config_name)

    if configs:
        for key in configs['configs'][config_name]:
            value = configs['configs'][config_name][key]
        app.config[key] = value


    # app.logger.info(app.config)
    
    migrate.init_app(app, db)
    db.init_app(app)
    ma.init_app(app)
    login_manager.init_app(app)
    csrf = CSRFProtect(app)  # noqa
    mail = Mail()
    mail.init_app(app)



    configure_uploads(app, categoryphotos)
    configure_uploads(app, subcategoryphotos)
    configure_uploads(app, productphotos)


    #
    # dev static
    #

    @app.route("/devstatic/<path:boxormodule>/f/<path:filename>")
    def devstatic(boxormodule, filename):
        if app.config["DEBUG"]:
            module_static = os.path.join(modules_path, boxormodule, "static")
            return send_from_directory(module_static, filename=filename)

    available_everywhere_entities = {}

    #
    #  load blueprints
    #
    for folder in os.listdir(os.path.join(base_path, "modules")):
        if folder.startswith("__"):  # ignore __pycache__
            continue

        if folder.startswith("box__"):
            # boxes
            for sub_folder in os.listdir(
                os.path.join(base_path, "modules", folder)
            ):
                if sub_folder.startswith("__"):  # ignore __pycache__
                    continue
                elif sub_folder.endswith(".json"):  # box_info.json
                    continue

                sys.path.insert(0, base_path)
                sys_mod = importlib.import_module(
                    "modules.{}.{}.view".format(folder, sub_folder)
                )
                print('module', folder, sub_folder, file=open('file.log', 'a'), flush=True)
                try:
                    sys.path.insert(0, base_path)
                    mod_global = importlib.import_module(
                        "modules.{}.{}.global".format(folder, sub_folder)
                    )
                    available_everywhere_entities.update(
                        mod_global.available_everywhere
                    )
                    print('module', mod_global.available_everywhere, file=open('file.log', 'a'), flush=True)
                except ImportError as e:
                    # print(e)
                    print(e, file=open('file.log', 'a'), flush=True)
                    pass
                app.register_blueprint(
                    getattr(sys_mod, "{}_blueprint".format(sub_folder))
                )
        else:
            # apps
            sys.path.insert(0, base_path)
            mod = importlib.import_module("modules.{}.view".format(folder))
            print('module', folder, file=open('file.log', 'a'), flush=True)
            try:
                sys.path.insert(0, base_path)
                mod_global = importlib.import_module(
                    "modules.{}.global".format(folder)
                )
                available_everywhere_entities.update(
                    mod_global.available_everywhere
                )

                print(mod_global.available_everywhere, file=open('file.log', 'a'), flush=True)
            except ImportError as e:
                # e
                print(e, file=open('file.log', 'a'), flush=True)
                pass
            app.register_blueprint(getattr(mod, "{}_blueprint".format(folder)))

    #
    # custom templates folder
    #
    with app.app_context():
        front_theme_dir = os.path.join(
            app.config["BASE_DIR"], "static", "themes", "front"
        )
        back_theme_dir = os.path.join(
            app.config["BASE_DIR"], "static", "themes", "back"
        )
        my_loader = jinja2.ChoiceLoader(
            [
                app.jinja_loader,
                jinja2.FileSystemLoader([front_theme_dir, back_theme_dir]),
            ]
        )
        app.jinja_loader = my_loader

    #
    # global vars
    #
    @app.context_processor
    def inject_global_vars():
        # theme_dir = os.path.join(
        #     app.config["BASE_DIR"], "themes", get_setting("ACTIVE_FRONT_THEME")
        # )
        # info_path = os.path.join(theme_dir, "info.json")
        # with open(info_path) as f:
        #     info_data = json.load(f)
        sys.path.insert(0, base_path)
        from modules.box__default.settings.helpers import get_setting

        APP_NAME = get_setting("APP_NAME")
        SECTION_NAME = get_setting("SECTION_NAME")
        SECTION_ITEMS = get_setting("SECTION_ITEMS")
        # ACTIVE_FRONT_THEME = get_setting("ACTIVE_FRONT_THEME")
        # ACTIVE_FRONT_THEME_VERSION = info_data["version"]
        # ACTIVE_FRONT_THEME_STYLES_URL = url_for(
        #     "resource.active_theme_css",
        #     active_theme=ACTIVE_FRONT_THEME,
        #     v=ACTIVE_FRONT_THEME_VERSION,
        # )

        base_context = {
            "APP_NAME": APP_NAME,
            "SECTION_NAME": SECTION_NAME,
            "SECTION_ITEMS": SECTION_ITEMS,
            # "ACTIVE_FRONT_THEME": ACTIVE_FRONT_THEME,
            # "ACTIVE_FRONT_THEME_VERSION": ACTIVE_FRONT_THEME_VERSION,
            # "ACTIVE_FRONT_THEME_STYLES_URL": ACTIVE_FRONT_THEME_STYLES_URL,
            "len": len,
            "current_user": current_user,
        }
        base_context.update(available_everywhere_entities)

        app.logger.info(available_everywhere_entities)


        return base_context

    print(available_everywhere_entities, file=open('file.log', 'a'), flush=True)
    # end of func
    return app

    # app.jinja_env.globals.update(x=x)
    # if app.config["DEBUG"]:
    # @app.after_request
    # def after_request(response):
    # response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate, public, max-age=0"
    # response.headers["Expires"] = 0
    # response.headers["Pragma"] = "no-cache"
    # return response


with open(os.path.join(base_path, 'config.json')) as f:
    config_json = json.load(f)
environment = config_json['environment']

app = create_app(environment, configs=config_json)


if __name__ == "__main__":

    app.run(debug=False, host="0.0.0.0")
