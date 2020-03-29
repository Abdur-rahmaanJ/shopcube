from functools import wraps
import importlib
import os

from flask import Flask, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
from werkzeug.utils import import_string
from werkzeug.utils import find_modules

from addon import db, login_manager, ma
from config import app_config


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(app_config[config_name])

    db.init_app(app)
    ma.init_app(app)
    login_manager.init_app(app)
    csrf = CSRFProtect(app)


    for module in os.listdir('modules'):
        if module.startswith('__'):
            continue
        mod = importlib.import_module('modules.{}.view'.format(module))
        app.register_blueprint(getattr(mod, '{}_blueprint'.format(module)))


    @app.route('/')
    def index():
        return redirect(app_config[config_name].HOMEPAGE_URL)

    return app


app = create_app('development')


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
