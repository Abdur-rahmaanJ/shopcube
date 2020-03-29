import os
import json

from flask import (
        Blueprint, 
        render_template, 
        request, 
        redirect, 
        jsonify
)
from flask_login import login_required, current_user
from flask_marshmallow import Marshmallow

from addon import db, ma
from modules.appointment.models import Appointments
from project_api import base_context


control_panel_blueprint = Blueprint('control_panel', __name__,
                                  template_folder='templates',
                                  url_prefix='/control_panel'
                                  )
all_info = {}

@control_panel_blueprint.route("/")
@login_required
def index():
    context = base_context()

    for module in os.listdir('modules'):
        if module.startswith('__'):
            continue
        if module not in ['control_panel']:
            with open('modules/{}/info.json'.format(module)) as f:
                module_info = json.loads(f.read())
                all_info[module] = module_info

    context['all_info'] = all_info
    return render_template('control_panel/index.html', **context)