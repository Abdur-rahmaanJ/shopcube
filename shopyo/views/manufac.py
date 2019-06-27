from flask import (
    Blueprint, render_template, request, redirect, url_for
    )
from models import db, Manufacturers, Settings
from flask_sqlalchemy import sqlalchemy
from settings import get_value

manufac_blueprint = Blueprint('manufac', __name__, url_prefix='/manufac')


@manufac_blueprint.route("/")
def manufac():
    return render_template('manufac_index.html', manufacs=Manufacturers.query.all(), OUR_APP_NAME=get_value('OUR_APP_NAME'),
        SECTION_NAME=get_value('SECTION_NAME'))


@manufac_blueprint.route('/add', methods=['GET', 'POST'])
def manufac_add():
    if request.method == 'POST':
        name = request.form['name']
        m = Manufacturers(name=name)
        db.session.add(m)
        db.session.commit()
        return redirect('/manufac/add')
    return render_template('manufac_add.html', OUR_APP_NAME=get_value('OUR_APP_NAME'))


@manufac_blueprint.route('/delete/<name>', methods=['GET', 'POST'])
def manufac_delete(name):
    Manufacturers.query.filter(Manufacturers.name == name).delete()
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
            render_template('manufac_message.html', 
                message="you cannot modify to an already existing manufacturer",
                redirect_url="/manufac/", OUR_APP_NAME=get_value('OUR_APP_NAME'), 
                SECTION_NAME=get_value('SECTION_NAME'))
        #return redirect(url_for('edit', barcode=barcode))
        return redirect('/manufac/')


@manufac_blueprint.route('/edit/<manufac_name>', methods=['GET', 'POST'])
def manufac_edit(manufac_name):
    m = Manufacturers.query.get(manufac_name)
    return render_template(
        'manufac_edit.html', manufac=manufac_name, OUR_APP_NAME=get_value('OUR_APP_NAME'), 
        SECTION_NAME=get_value('SECTION_NAME'))