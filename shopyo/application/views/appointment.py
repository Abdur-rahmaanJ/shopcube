from flask import (
    Blueprint, render_template, request, redirect
)

from models import db, Appointments
from settings import get_value

appointment_blueprint = Blueprint('appointment', __name__, url_prefix='/appointment')


@appointment_blueprint.route("/")
def appointment_main():
    return render_template('appointment_index.html', appointments=Appointments.query.all(),
                           OUR_APP_NAME=get_value('OUR_APP_NAME'), SECTION_NAME=get_value('SECTION_NAME'))


@appointment_blueprint.route('/add', methods=['GET', 'POST'])
def appointment_add():
    if request.method == 'POST':
        name = request.form['name']
        time = request.form['time']
        m = Appointments(name=name, time=time)
        db.session.add(m)
        db.session.commit()
        return redirect('/appointment/add')
    return render_template('appointment_add.html', OUR_APP_NAME=get_value('OUR_APP_NAME'))


@appointment_blueprint.route('/delete/<ids>', methods=['GET', 'POSE'])
def appointment_delete(ids):
    Appointments.query.filter(Appointments.id == ids).delete()
    db.session.commit()
    return redirect('/appointment')


@appointment_blueprint.route('/edit/<ids>', methods=['GET', 'POSE'])
def appointment_edit(ids):
    a = Appointments.query.get(ids)
    return render_template('appointment_edit.html', id=a.id, name=a.name, time=a.time,
                           OUR_APP_NAME=get_value('OUR_APP_NAME'), SECTION_ITEMS=get_value('SECTION_ITEMS'))
