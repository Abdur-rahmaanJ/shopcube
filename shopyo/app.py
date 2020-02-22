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

    from views.manufac import manufac_blueprint
    from views.products import prod_blueprint
    from views.settings_modif import settings_blueprint
    from views.appointment import appointment_blueprint
    from views.people import people_blueprint
    from views.admin_modif import admin_blueprint
    from views.login import login_blueprint
    from views.save import save_blueprint

    app.register_blueprint(manufac_blueprint)
    app.register_blueprint(prod_blueprint)
    app.register_blueprint(settings_blueprint)
    app.register_blueprint(appointment_blueprint)
    app.register_blueprint(people_blueprint)
    app.register_blueprint(admin_blueprint)
    app.register_blueprint(login_blueprint)
    app.register_blueprint(save_blueprint)

    @app.route('/')
    def index():
        return redirect(app_config[config_name].HOMEPAGE_URL)

    return app


app = create_app('development')


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')

