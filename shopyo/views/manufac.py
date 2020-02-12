from flask import (
    Blueprint, render_template, request, redirect, url_for, jsonify
    )
from flask_sqlalchemy import sqlalchemy
from addon import db
from models import Manufacturers, Products, Settings, Appointments
#from app import db

from flask_login import login_required, current_user

from project_api import base_context
from sqlalchemy import exists

manufac_blueprint = Blueprint('manufac', __name__, url_prefix='/manufac')

@manufac_blueprint.route("/")
@login_required
def manufac():
    context = base_context()

    context['manufacs'] = Manufacturers.query.all()
    return render_template('manufac/index.html', **context)


@manufac_blueprint.route('/add', methods=['GET', 'POST'])
@login_required
def manufac_add():
    context = base_context()

    has_manufac = False
    if request.method == 'POST':
        name = request.form['name']
        has_manufac = db.session.query(exists().where(Manufacturers.name == name)).scalar()
        if has_manufac == False:
            m = Manufacturers(name=name)
            db.session.add(m)
            db.session.commit()
        return render_template('manufac/add.html', **context)

    context['has_manufac'] = str(has_manufac)
    return render_template('manufac/add.html', **context)


@manufac_blueprint.route('/delete/<name>', methods=['GET', 'POST'])
@login_required
def manufac_delete(name):
    Manufacturers.query.filter(Manufacturers.name == name).delete()
    Products.query.filter(Products.manufacturer == name).delete()
    db.session.commit()
    return redirect('/manufac')


@manufac_blueprint.route('/update', methods=['GET', 'POST'])
@login_required
def manufac_update():
    context = base_context()

    if request.method == 'POST': #this block is only entered when the form is submitted
        name = request.form['manufac_name']
        old_name = request.form['old_manufac_name']
        try:
            m = Manufacturers.query.get(old_name)
            m.name = name
            products = Products.query.filter_by(manufacturer=old_name)
            for product in products:
                product.manufacturer = name
            db.session.commit()
        except sqlalchemy.exc.IntegrityError:
            # return redirect('/manufac/')
            context['message'] = "you cannot modify to an already existing manufacturer"
            context['redirect_url'] = "/manufac/"
            render_template('manufac/message.html', **context)
        #return redirect(url_for('edit', barcode=barcode))
        return redirect('/manufac/')


@manufac_blueprint.route('/edit/<manufac_name>', methods=['GET', 'POST'])
@login_required
def manufac_edit(manufac_name):
    context = base_context()

    m = Manufacturers.query.get(manufac_name)
    context['manufac_name'] = manufac_name
    return render_template('manufac/edit.html', **context)

# api
@manufac_blueprint.route("/check/<manufac_name>", methods=["GET"])
@login_required
def check(manufac_name):
    has_manufac = db.session.query(exists().where(Manufacturers.name == manufac_name)).scalar()
    return jsonify({"exists":has_manufac})
