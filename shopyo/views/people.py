from flask import (
    Blueprint, render_template, request, redirect
)

from models import db, People
from settings import get_value
import datetime

people_blueprint = Blueprint('people', __name__, url_prefix='/people')


@people_blueprint.route("/")
def people_main():
    return render_template('people/index.html', peoples=People.query.all(),
                           OUR_APP_NAME=get_value('OUR_APP_NAME'), SECTION_NAME=get_value('SECTION_NAME'))


@people_blueprint.route('/add', methods=['GET', 'POST'])
def people_add():
    if request.method == 'POST':
        name = request.form['name']
        birthday = request.form['birthday']
        about = request.form['about']
        social_media = request.form['social_media']
        # calculate age
        today_date = datetime.datetime.now()
        time_format = "%Y-%m-%d"
        b_day = datetime.datetime.strptime(birthday, time_format)
        age = str(today_date - b_day)
        # insert data into DB
        p = People(name=name, birthday=birthday, age=age,
                   about=about, social_media=social_media)
        db.session.add(p)
        db.session.commit()
        return redirect('/people/add')
    return render_template('people/add.html', OUR_APP_NAME=get_value('OUR_APP_NAME'), message='')


@people_blueprint.route('/delete/<id>', methods=['GET', 'POST'])
def people_delete(id):
    People.query.filter(People.id == id).delete()
    db.session.commit()
    return redirect('/people')


@people_blueprint.route('/edit/<name>', methods=['GET', 'POST'])
def people_edit(name):
    a = People.query.get(name)
    return render_template('people/edit.html',
                           id=a.id, name=a.name, birthday=a.birthday, about=a.about, social_media=a.social_media,
                           OUR_APP_NAME=get_value('OUR_APP_NAME'), SECTION_ITEMS=get_value('SECTION_ITEMS'))


@people_blueprint.route('/update', methods=['GET', 'POST'])
def people_update():
    people_name = request.form['name']
    people_id = request.form['id']
    people_birthday = request.form['birthday']
    people_about = request.form['about']
    people_social_media = request.form['social_media']
    # calculate age
    today_date = datetime.datetime.now()
    time_format = "%Y-%m-%d"
    b_day = datetime.datetime.strptime(people_birthday, time_format)
    people_age = str(today_date - b_day)
    # retrive record from db with id
    s = People.query.get(people_id)
    s.name = people_name
    s.birthday = people_birthday
    s.age = people_age
    s.about = people_about
    s.social_media = people_social_media
    db.session.commit()
    return redirect('/people')
