from flask import (
    Blueprint, render_template, request, redirect, url_for, jsonify
    )
from addon import db
from views.settings.models import Settings
from flask_marshmallow import Marshmallow
from flask_login import login_required, current_user

from project_api import base_context

settings_blueprint = Blueprint('settings', __name__, url_prefix='/settings')

@settings_blueprint.route("/")
@login_required
def settings_main():
    context = base_context()

    settings =  Settings.query.all()

    context['settings'] = settings
    return render_template('settings/index.html', **context)


@settings_blueprint.route('/edit/<settings_name>', methods=['GET', 'POST'])
@login_required
def settings_edit(settings_name):
    context = base_context()

    s = Settings.query.get(settings_name)
    
    context['settings_name'] = settings_name
    context['current_value'] = s.value

    return render_template('settings/edit.html', **context)

@settings_blueprint.route('/update', methods=['GET', 'POST'])
@login_required
def settings_update():
    context = base_context()

    settings_name = request.form['settings_name']
    settings_value = request.form['settings_value']
    s = Settings.query.get(settings_name)
    s.value = settings_value
    db.session.commit()
    settings =  Settings.query.all()

    context['settings'] = settings
    return render_template('settings/index.html', **context)