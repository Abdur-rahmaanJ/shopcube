from flask import (
    Blueprint, render_template, request, redirect, url_for, jsonify
    )
from addon import db
from models import Settings
#from app import app, db
from flask_marshmallow import Marshmallow
from flask_login import login_required, current_user

from settings import get_value

settings_blueprint = Blueprint('settings', __name__, url_prefix='/settings')

@settings_blueprint.route("/")
@login_required
def settings_main():
    settings =  Settings.query.all()
    return render_template('settings/index.html', settings=settings, OUR_APP_NAME=get_value('OUR_APP_NAME'))

@settings_blueprint.route('/edit/<settings_name>', methods=['GET', 'POST'])
@login_required
def settings_edit(settings_name):
    s = Settings.query.get(settings_name)
    return render_template(
        'settings/edit.html', settings_name=settings_name, current_value=s.value, OUR_APP_NAME=get_value('OUR_APP_NAME'))

@settings_blueprint.route('/update', methods=['GET', 'POST'])
@login_required
def settings_update():
    settings_name = request.form['settings_name']
    settings_value = request.form['settings_value']
    s = Settings.query.get(settings_name)
    s.value = settings_value
    db.session.commit()
    settings =  Settings.query.all()
    return render_template('settings/index.html', settings=settings, OUR_APP_NAME=get_value('OUR_APP_NAME'))