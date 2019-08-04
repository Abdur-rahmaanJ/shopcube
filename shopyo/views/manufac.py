from flask import (
    Blueprint, render_template, request, redirect, url_for, jsonify
    )
from models import Manufacturers, Products, Settings, Appointments
from app import db
from flask_sqlalchemy import sqlalchemy
from settings import get_value
from sqlalchemy import exists

manufac_blueprint = Blueprint('manufac', __name__, url_prefix='/manufac')

@manufac_blueprint.route("/")
def manufac():
    return render_template('manufac/index.html', manufacs=Manufacturers.query.all(), OUR_APP_NAME=get_value('OUR_APP_NAME'),
        SECTION_NAME=get_value('SECTION_NAME'))


@manufac_blueprint.route('/add', methods=['GET', 'POST'])
def manufac_add():
    has_manufac = False
    if request.method == 'POST':
        name = request.form['name']
        has_manufac = db.session.query(exists().where(Manufacturers.name == name)).scalar()
        if has_manufac == False:
            m = Manufacturers(name=name)
            db.session.add(m)
            db.session.commit()
        return render_template(
                    'manufac/add.html', 
                    OUR_APP_NAME=get_value('OUR_APP_NAME'),
                    has_manufac=str(has_manufac))
    return render_template(
                'manufac/add.html', 
                OUR_APP_NAME=get_value('OUR_APP_NAME'),
                has_manufac=str(has_manufac))


@manufac_blueprint.route('/delete/<name>', methods=['GET', 'POST'])
def manufac_delete(name):
    Manufacturers.query.filter(Manufacturers.name == name).delete()
    Products.query.filter(Products.manufacturer == name).delete()
    db.session.commit()
    return redirect('/manufac')


@manufac_blueprint.route('/update', methods=['GET', 'POST'])
def manufac_update():
    if request.method == 'POST': #this block is only entered when the form is submitted
        name = request.form['manufac_name']
        old_name = request.form['old_manufac_name']
        try:
            m = Manufacturers.query.get(old_name)
            m.name = name
            db.session.commit()
        except sqlalchemy.exc.IntegrityError:
            # return redirect('/manufac/')
            render_template('manufac/message.html', 
                message="you cannot modify to an already existing manufacturer",
                redirect_url="/manufac/", OUR_APP_NAME=get_value('OUR_APP_NAME'), 
                SECTION_NAME=get_value('SECTION_NAME'))
        #return redirect(url_for('edit', barcode=barcode))
        return redirect('/manufac/')


@manufac_blueprint.route('/edit/<manufac_name>', methods=['GET', 'POST'])
def manufac_edit(manufac_name):
    m = Manufacturers.query.get(manufac_name)
    return render_template('manufac/edit.html', manufac=manufac_name, OUR_APP_NAME=get_value('OUR_APP_NAME'), 
        SECTION_NAME=get_value('SECTION_NAME'))

# api 
@manufac_blueprint.route("/check/<manufac_name>", methods=["GET"])
def check(manufac_name):
    has_manufac = db.session.query(exists().where(Manufacturers.name == manufac_name)).scalar()
    return jsonify({"exists":has_manufac})