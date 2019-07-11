from flask import (
    Blueprint, render_template, request, redirect, url_for, jsonify
    )
from models import app, db, People, Settings, Products
from flask_marshmallow import Marshmallow
from settings import get_value

person_blueprint = Blueprint('people', __name__, url_prefix='/people')

ma = Marshmallow(app)

class PersonSchema(ma.Schema):
    class Meta:
        # Fields to expose
        fields = ('name', 'age', 'birthday', 'about', 'social media')

person_schema = PersonSchema()
person_schema = PersonSchema(many=True)


@person_blueprint.route("/list_people")
def list_people():
    people = People.query
    return render_template('people_list.html', people=people, 
        OUR_APP_NAME=get_value('OUR_APP_NAME'), SECTION_ITEMS=get_value('SECTION_ITEMS'),
        SECTION_NAME=get_value('SECTION_NAME'))


@person_blueprint.route('/add', methods=['GET', 'POST'])
def people_add():
    if request.method == 'POST':
        name = request.form['name']
        birthday = request.form['birthday']
        age = age_from_birthday(birthday)
        about = request.form['about']
        social_media = request.form['social_media']
        p = People(name=name, about=about, birthday=birthday,
            social_media=social_media, age=age)
        db.session.add(p)
        db.session.commit()
        return redirect('/people/add')
    return render_template('people_add.html', OUR_APP_NAME=get_value('OUR_APP_NAME'),
        SECTION_ITEMS=get_value('SECTION_ITEMS'))


@person_blueprint.route('/delete/<person_name>', methods=['GET', 'POST'])
def people_delete(person_name):
    People.query.filter(
        People.name == person_name).delete()
    db.session.commit()
    return redirect('/people/list_people')


@person_blueprint.route('/edit/<person_name>', methods=['GET', 'POST'])
def people_edit(person_name):
    p = People.query.filter(
        People.name == person_name).first()
    return render_template(
        'people_edit.html', name=p.name, birthday=p.birthday,
        about=p.about, social_media=p.social_media, OUR_APP_NAME=get_value('OUR_APP_NAME'),
        SECTION_ITEMS=get_value('SECTION_ITEMS'))


@person_blueprint.route('/update', methods=['GET', 'POST'])
def people_update():
    if request.method == 'POST': #this block is only entered when the form is submitted
        name = request.form['name']
        oldname = request.form['oldname']
        birthday = request.form['birthday']
        age = age_from_birthday(birthday)
        about = request.form['about']
        social_media = request.form['social_media']

        p = People.query.filter(
            People.name == oldname 
        ).first()
        p.name = name
        p.birthday = birthday
        p.about = about
        p.social_media = social_media
        p.age = age
        db.session.commit()
        return redirect('/people/list_people')

@person_blueprint.route("/lookup/<manufac_name>")
def lookup_people(manufac_name):
    return render_template('people_lookup.html', manufac=manufac_name, OUR_APP_NAME=get_value('OUR_APP_NAME'),
        SECTION_ITEMS=get_value('SECTION_ITEMS'))

# api
@person_blueprint.route("/search/<manufac_name>/barcode/<barcode>", methods=["GET"])
def search(manufac_name, barcode):
    all_p = Products.query.filter(
            (Products.barcode.like('%'+barcode+'%')) & (Products.manufacturer == manufac_name)
        ).all()
    result = product_schema.dump(all_p)
    return jsonify(result.data)


def age_from_birthday(birthday):
    fields = birthday.split('-')
    from datetime import date
    today = date.today()
    return today.year - int(fields[0]) - ((today.month, today.day) < (int(fields[1]), int(fields[2])))
