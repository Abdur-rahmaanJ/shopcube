import importlib
import os
import sys

from flask import Flask
from flask import redirect

from flask_wtf.csrf import CSRFProtect


import sys

sys.path.append(".")

from flask_uploads import configure_uploads

from config import app_config

from shopyoapi.init import db
from shopyoapi.init import login_manager
from shopyoapi.init import ma
from shopyoapi.init import migrate
from shopyoapi.init import productphotos

base_path = os.path.dirname(os.path.abspath(__file__))


def create_app(config_name):
    app = Flask(__name__)
    configuration = app_config[config_name]
    app.config.from_object(configuration)
    migrate.init_app(app, db)
    db.init_app(app)
    ma.init_app(app)
    login_manager.init_app(app)
    csrf = CSRFProtect(app)  # noqa

    configure_uploads(app, productphotos)

    for module in os.listdir(os.path.join(base_path, "modules")):
        if module.startswith("__"):
            continue
        mod = importlib.import_module("modules.{}.view".format(module))
        app.register_blueprint(getattr(mod, "{}_blueprint".format(module)))

    @app.route("/")
    def index():
        return redirect(configuration.HOMEPAGE_URL)

    return app


app = create_app("development")


if __name__ == "__main__":

    app.run(debug=False, host="0.0.0.0")
