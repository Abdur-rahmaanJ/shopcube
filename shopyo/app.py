from functools import wraps

from flask import Flask, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect

from addon import db, login_manager, ma
from config import app_config


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(app_config[config_name])

    db.init_app(app)
    ma.init_app(app)
    login_manager.init_app(app)
    csrf = CSRFProtect(app)

    from modules.manufacturer.manufac import manufac_blueprint
    from modules.products.products import prod_blueprint
    from modules.settings.settings_modif import settings_blueprint
    from modules.appointment.appointment import appointment_blueprint
    from modules.people.people import people_blueprint
    from modules.admin.admin_modif import admin_blueprint
    from modules.login.login import login_blueprint
    from modules.save.save import save_blueprint
    from modules.base.base import base_blueprint

    app.register_blueprint(manufac_blueprint)
    app.register_blueprint(prod_blueprint)
    app.register_blueprint(settings_blueprint)
    app.register_blueprint(appointment_blueprint)
    app.register_blueprint(people_blueprint)
    app.register_blueprint(admin_blueprint)
    app.register_blueprint(login_blueprint)
    app.register_blueprint(save_blueprint)
    app.register_blueprint(base_blueprint)

    @app.route('/')
    def index():
        return redirect(app_config[config_name].HOMEPAGE_URL)

    return app


app = create_app('development')


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
