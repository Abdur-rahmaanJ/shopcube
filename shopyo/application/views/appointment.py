from flask import (
    Blueprint, render_template, request, redirect, url_for
)
from models import app, db, Settings, Appointments
from flask_marshmallow import Marshmallow
from settings import get_value

appointment_blueprint = Blueprint('appointment', __name__, url_prefix='/appointment')

@appointment_blueprint.route("/")
def appointment_main():
    #appointments = Appointments.query.all()
    return render_template('appointment_index.html')

@appointment_blueprint.route('/add', methods=['GET', 'POST'])
def appointment_add():
    if request.method == 'POST':
        name = request.form['name']
        m = Appointments(name=name)
        db.session.add(m)
        db.session.commit()
        return redirect('/appointment/add')
    return render_template('appointment_add.html', OUR_APP_NAME=get_value('OUR_APP_NAME'))
