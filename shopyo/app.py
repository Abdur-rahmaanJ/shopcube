import importlib
import os

from flask import Flask, redirect
from flask_wtf.csrf import CSRFProtect
from shopyoapi.init import db, login_manager, ma
from config import app_config

base_path = os.path.dirname(os.path.abspath(__file__))
def create_app(config_name):
    app = Flask(__name__)
    configuration = app_config[config_name]
    app.config.from_object(configuration)

    db.init_app(app)
    ma.init_app(app)
    login_manager.init_app(app)
    csrf = CSRFProtect(app)  # noqa
    
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
    
    app.run(debug=True, host="0.0.0.0")
