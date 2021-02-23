import importlib
import os
import json
import jinja2
from flask import Flask
from flask import send_from_directory
from flask import redirect
from flask import url_for
from flask import request
from flask_login import current_user
from flask_wtf.csrf import CSRFProtect
from flask_uploads import configure_uploads
from flask_admin import Admin
from flask_admin.contrib import sqla as flask_admin_sqla
from flask_admin import AdminIndexView
from flask_admin import expose
from flask_admin.menu import MenuLink

from modules.box__default.settings.helpers import get_setting
from modules.box__default.settings.models import Settings

from shopyoapi.init import categoryphotos
from shopyoapi.init import db
from shopyoapi.init import login_manager
from shopyoapi.init import ma
from shopyoapi.init import migrate
from shopyoapi.init import mail
from shopyoapi.init import productphotos
from shopyoapi.init import subcategoryphotos
from shopyoapi.path import modules_path
from shopyoapi.file import trycopy

#
# Flask admin setup
#


class DefaultModelView(flask_admin_sqla.ModelView):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def is_accessible(self):
        return current_user.is_authenticated and current_user.is_admin

    def inaccessible_callback(self, name, **kwargs):
        # redirect to login page if user doesn't have access
        return redirect(url_for('auth.login', next=request.url))


class MyAdminIndexView(AdminIndexView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.is_admin

    def inaccessible_callback(self, name, **kwargs):
        # redirect to login page if user doesn't have access
        return redirect(url_for('auth.login', next=request.url))

    @expose('/')
    def index(self):
        if not current_user.is_authenticated and current_user.is_admin:
            return redirect(url_for('auth.login'))
        return super(MyAdminIndexView, self).index()

    @expose('/dashboard')
    def indexs(self):
        if not current_user.is_authenticated and current_user.is_admin:
            return redirect(url_for('auth.login'))
        return super(MyAdminIndexView, self).index()

#
# secrets files
#


try:
    if not os.path.exists('config.py'):
        trycopy('config_demo.py', 'config.py')
    if not os.path.exists('config.json'):
        trycopy('config_demo.json', 'config.json')
except PermissionError as e:
    print(
        'Cannot continue, permission error'
        'initializing config.py and config.json, '
        'copy and rename them yourself!'
    )
    raise e

from config import app_config

base_path = os.path.dirname(os.path.abspath(__file__))


def create_app(config_name):
    # from modules.box__default.settings.helpers import Settings
    app = Flask(__name__)
    configuration = app_config[config_name]
    app.config.from_object(configuration)
    migrate.init_app(app, db)
    db.init_app(app)
    ma.init_app(app)
    mail.init_app(app)
    login_manager.init_app(app)
    csrf = CSRFProtect(app)  # noqa

    configure_uploads(app, categoryphotos)
    configure_uploads(app, subcategoryphotos)
    configure_uploads(app, productphotos)

    admin = Admin(
        app,
        name='My App',
        template_mode='bootstrap4',
        index_view=MyAdminIndexView()
    )
    admin.add_view(DefaultModelView(Settings, db.session))
    admin.add_link(MenuLink(name='Logout', category='', url='/auth/logout?next=/admin'))

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
    # load blueprints
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
                try:
                    sys_mod = importlib.import_module(
                        "modules.{}.{}.view".format(folder, sub_folder)
                    )
                    app.register_blueprint(
                        getattr(sys_mod, "{}_blueprint".format(sub_folder))
                    )
                except AttributeError as e:
                    print(' x Blueprint skipped:', 'modules.{}.{}.view'.format(folder, sub_folder, folder))
                    pass
                try:
                    mod_global = importlib.import_module(
                        "modules.{}.{}.global".format(folder, sub_folder)
                    )
                    available_everywhere_entities.update(
                        mod_global.available_everywhere
                    )
                except ImportError as e:
                    # print(e)
                    pass

        else:
            # apps
            try:
                mod = importlib.import_module("modules.{}.view".format(folder))
                app.register_blueprint(getattr(mod, "{}_blueprint".format(folder)))
            except AttributeError as e:
                    print('[ ] Blueprint skipped:', e)
                    pass
            try:
                mod_global = importlib.import_module(
                    "modules.{}.global".format(folder)
                )
                available_everywhere_entities.update(
                    mod_global.available_everywhere
                )
            except ImportError as e:
                # print(e)
                pass

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

        # print('\nav everywhere entities\n', available_everywhere_entities)

        return base_context

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
app = create_app(environment)


if __name__ == "__main__":

    app.run(debug=False, host="0.0.0.0")
