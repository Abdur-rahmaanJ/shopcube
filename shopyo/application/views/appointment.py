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
        date = request.form['date']
        active = request.form['active']
        time = request.form['time']
        m = Appointments(name=name, date=date, time=time, active=active)
        db.session.add(m)
        db.session.commit()
        return redirect('/appointment/add')
    return render_template('appointment_add.html', OUR_APP_NAME=get_value('OUR_APP_NAME'))


@appointment_blueprint.route('/delete/<ids>', methods=['GET', 'POST'])
def appointment_delete(ids):
    Appointments.query.filter(Appointments.id == ids).delete()
    db.session.commit()
    return redirect('/appointment')


@appointment_blueprint.route('/edit/<ids>', methods=['GET', 'POST'])
def appointment_edit(ids):
    a = Appointments.query.get(ids)
    return render_template('appointment_edit.html', 
                           id=a.id, name=a.name, date=a.date,
                           time=a.time, active=a.active,
                           OUR_APP_NAME=get_value('OUR_APP_NAME'), SECTION_ITEMS=get_value('SECTION_ITEMS'))


@appointment_blueprint.route('/update', methods=['GET', 'POST'])
def appointment_update():
    appointment_name = request.form['appointment_name']
    appointment_date = request.form['appointment_date']
    appointment_time = request.form['appointment_time']
    appointment_id = request.form['appointment_id']
    appointment_active = request.form['appointment_active']
    s = Appointments.query.get(appointment_id)
    s.name = appointment_name
    s.date = appointment_date
    s.time = appointment_time
    s.active = appointment_active
    db.session.commit()
    return redirect('/appointment')


@appointment_blueprint.route('/active/<ids>', methods=['GET', 'POST'])
def active(ids):
    s = Appointments.query.get(ids)
    s.active = "active"
    db.session.commit()
    return redirect('/appointment')


@appointment_blueprint.route('/inactive/<ids>', methods=['GET', 'POST'])
def deactive(ids):
    s = Appointments.query.get(ids)
    s.active = "inactive"
    db.session.commit()
    return redirect('/appointment')
