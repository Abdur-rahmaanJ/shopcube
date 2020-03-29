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

@control_panel_blueprint.route("/")
@login_required
def index():
    context = base_context()
    
    return render_template('control_panel/index.html', **context)