import json
import os

from flask import Blueprint
from flask import jsonify
from flask import redirect
from flask import render_template
from flask import request

from flask_login import login_required

from init import db
from init import ma

from modules.box__bizhelp.appointment.models import Appointments

dirpath = os.path.dirname(os.path.abspath(__file__))
module_info = {}

with open(dirpath + "/info.json") as f:
    module_info = json.load(f)

appointment_blueprint = Blueprint(
    "appointment",
    __name__,
    template_folder="templates",
    url_prefix=module_info["url_prefix"],
)


class AppointmentSchema(ma.Schema):
    class Meta:
        # Fields to expose
        fields = ("id", "name", "date", "time", "active")


appointment_schema = AppointmentSchema()
appointment_schema = AppointmentSchema(many=True)


@appointment_blueprint.route("/")
@login_required
def index():
    context = {}

    context["appointments"] = Appointments.query.all()
    return render_template("appointment/index.html", **context)


@appointment_blueprint.route("/add", methods=["GET", "POST"])
@login_required
def add():
    context = {}

    if request.method == "POST":
        name = request.form["name"]
        date = request.form["date"]
        active = request.form["active"]
        time = request.form["time"]
        m = Appointments(name=name, date=date, time=time, active=active)
        db.session.add(m)
        db.session.commit()
        return redirect("/appointment/add")
    return render_template("appointment/add.html", **context)


@appointment_blueprint.route("/delete/<ids>", methods=["GET", "POST"])
@login_required
def appointment_delete(ids):
    Appointments.query.filter(Appointments.id == ids).delete()
    db.session.commit()
    return redirect("/appointment")


@appointment_blueprint.route("/edit/<ids>", methods=["GET", "POST"])
@login_required
def appointment_edit(ids):
    context = {}

    a = Appointments.query.get(ids)
    context["id"] = a.id
    context["name"] = a.name
    context["date"] = a.date
    context["time"] = a.time
    context["active"] = a.active
    return render_template("appointment/edit.html", **context)


@appointment_blueprint.route("/update", methods=["GET", "POST"])
@login_required
def appointment_update():
    appointment_name = request.form["appointment_name"]
    appointment_date = request.form["appointment_date"]
    appointment_time = request.form["appointment_time"]
    appointment_id = request.form["appointment_id"]
    appointment_active = request.form["appointment_active"]
    s = Appointments.query.get(appointment_id)
    s.name = appointment_name
    s.date = appointment_date
    s.time = appointment_time
    s.active = appointment_active
    db.session.commit()
    return redirect("/appointment")


@appointment_blueprint.route("/active/<ids>", methods=["GET", "POST"])
@login_required
def active(ids):
    s = Appointments.query.get(ids)
    s.active = "active"
    db.session.commit()
    return redirect("/appointment")


@appointment_blueprint.route("/inactive/<ids>", methods=["GET", "POST"])
@login_required
def deactive(ids):
    s = Appointments.query.get(ids)
    s.active = "inactive"
    db.session.commit()
    return redirect("/appointment")


@appointment_blueprint.route("/lookup", methods=["GET", "POST"])
@login_required
def lookup():
    context = {}
    context["appointments"] = Appointments.query.all()
    return render_template("appointment/lookup.html", **context)


# api
@appointment_blueprint.route("/search/name/<name>", methods=["GET", "POST"])
@login_required
def search_name(name):
    if name == "searchValueIsEmpty":
        all_a = Appointments.query.all()
    else:
        all_a = Appointments.query.filter(
            Appointments.name.like("%" + name + "%")
        ).all()
    result = appointment_schema.dump(all_a)
    return jsonify(result)
