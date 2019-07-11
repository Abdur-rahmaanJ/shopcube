from flask import (
    Blueprint, render_template
    )
from models import app, db, Settings
from flask_marshmallow import Marshmallow
from settings import get_value

appointment_blueprint = Blueprint('appointment', __name__, url_prefix='/appointment')

@appointment_blueprint.route("/")
def appointment_main():
    settings = Settings.query.all()
    return render_template('appointment_index.html', settings=settings, OUR_APP_NAME=get_value('OUR_APP_NAME'))



