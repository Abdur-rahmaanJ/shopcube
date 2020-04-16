import os
import json

from flask import Blueprint, render_template, request, redirect, jsonify
from flask_login import login_required
from datetime import date
from shopyoapi.init import db, ma
from modules.people.models import People

from shopyoapi.enhance import base_context
import datetime


dirpath = os.path.dirname(os.path.abspath(__file__))
module_info = {}

with open(dirpath + "/info.json") as f:
    module_info = json.load(f)

people_blueprint = Blueprint(
    "people",
    __name__,
    template_folder="templates",
    url_prefix=module_info["url_prefix"],
)


class PeopleSchema(ma.Schema):
    class Meta:
        # Fields to expose
        fields = (
            "id",
            "name",
            "phone",
            "mobile",
            "email",
            "facebook",
            "twitter",
            "linkedin",
            "age",
            "birthday",
            "notes",
        )


people_schema = PeopleSchema()
people_schema = PeopleSchema(many=True)


@people_blueprint.route("/")
def people_main():
    context = base_context()

    context["people"] = People.query.all()
    return render_template("people/index.html", **context)


@people_blueprint.route("/add", methods=["GET", "POST"])
def people_add():
    context = base_context()

    if request.method == "POST":
        name = request.form["name"]
        phone = request.form["phone"]
        mobile = request.form["mobile"]
        email = request.form["email"]
        linkedin = request.form["linkedin"]
        facebook = request.form["facebook"]
        twitter = request.form["twitter"]
        birthday = request.form["birthday"]
        notes = request.form["notes"]
        # calculate age
        today_date = date.today()
        date_format = "%Y-%m-%d"
        b_day = datetime.datetime.strptime(birthday, date_format)
        age = (
            today_date.year
            - b_day.year
            - ((today_date.month, today_date.day) < (b_day.month, b_day.day))
        )

        # insert data into DB
        person = People(
            name=name,
            phone=phone,
            mobile=mobile,
            email=email,
            linkedin=linkedin,
            facebook=facebook,
            twitter=twitter,
            age=age,
            birthday=birthday,
            notes=notes,
        )
        db.session.add(person)
        db.session.commit()
        return redirect("/people/add")
    context["message"] = ""
    return render_template("people/add.html", **context)


@people_blueprint.route("/delete/<id>", methods=["GET", "POST"])
def people_delete(id):
    People.query.filter(People.id == id).delete()
    db.session.commit()
    return redirect("/people")


@people_blueprint.route("/edit/<id>", methods=["GET", "POST"])
def people_edit(id):
    context = base_context()

    a = People.query.get(id)

    context["id"] = a.id
    context["name"] = a.name
    context["phone"] = a.phone
    context["mobile"] = a.mobile
    context["email"] = a.email
    context["linkedin"] = a.linkedin
    context["facebook"] = a.facebook
    context["twitter"] = a.twitter
    context["age"] = a.age
    context["birthday"] = a.birthday
    context["notes"] = a.notes
    return render_template("people/edit.html", **context)


@people_blueprint.route("/update", methods=["GET", "POST"])
def people_update():
    if request.method == "POST":
        people_id = request.form["id"]
        people_name = request.form["name"]
        people_phone = request.form["phone"]
        people_mobile = request.form["mobile"]
        people_email = request.form["email"]
        people_linkedin = request.form["linkedin"]
        people_facebook = request.form["facebook"]
        people_twitter = request.form["twitter"]
        people_birthday = request.form["birthday"]
        people_notes = request.form["notes"]

        # calculate age
        today_date = datetime.datetime.now()
        time_format = "%Y-%m-%d"
        b_day = datetime.datetime.strptime(people_birthday, time_format)
        people_age = str(today_date - b_day)
        # retrive record from db with id
        s = People.query.get(people_id)
        s.name = people_name
        s.phone = people_phone
        s.mobile = people_mobile
        s.email = people_email
        s.facebook = people_facebook
        s.linkedin = people_linkedin
        s.twitter = people_twitter
        s.birthday = people_birthday
        s.notes = people_notes
        s.age = people_age

        db.session.commit()

        return redirect("/people")


@people_blueprint.route("/lookup", methods=["GET", "POST"])
@login_required
def lookup():
    context = base_context()
    context["people"] = People.query.all()
    return render_template("people/lookup.html", **context)


# api
@people_blueprint.route("/search/name/<name>", methods=["GET", "POST"])
@login_required
def search_name(name):
    if name == "searchValueIsEmpty":
        all_a = People.query.all()
    else:
        all_a = People.query.filter(People.name.like("%" + name + "%")).all()
    result = people_schema.dump(all_a)
    return jsonify(result)
