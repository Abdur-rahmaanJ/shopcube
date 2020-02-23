from flask import (
    Blueprint, render_template, request, redirect, url_for, jsonify
    )
from flask_sqlalchemy import sqlalchemy
from views.manufacturer.models import Manufacturer


from flask_login import login_required, current_user

from project_api import base_context

manufac_blueprint = Blueprint('manufac', __name__, url_prefix='/manufac')

@manufac_blueprint.route("/")
@login_required
def manufac():
    context = base_context()
    context['manufacs'] = Manufacturer.query.all()
    return render_template('manufac/index.html', **context)


@manufac_blueprint.route('/add', methods=['GET', 'POST'])
@login_required
def manufac_add():
    context = base_context()

    has_manufac = False
    if request.method == 'POST':
        name = request.form['name']
        has_manufac = Manufacturer.manufacturer_exists(name)
        if has_manufac == False:
            m = Manufacturer(name=name)
            m.insert()
        return render_template('manufac/add.html', **context)

    context['has_manufac'] = str(has_manufac)
    return render_template('manufac/add.html', **context)


@manufac_blueprint.route('/delete/<name>', methods=['GET', 'POST'])
@login_required
def manufac_delete(name):
    manufac = Manufacturer.query.filter(Manufacturer.name == name).first()
    manufac.delete()
    return redirect('/manufac')


@manufac_blueprint.route('/update', methods=['GET', 'POST'])
@login_required
def manufac_update():
    context = base_context()

    if request.method == 'POST': #this block is only entered when the form is submitted
        name = request.form['manufac_name']
        old_name = request.form['old_manufac_name']
        try:
            m = Manufacturer.query.get(old_name)
            m.name = name
            m.update()
        except sqlalchemy.exc.IntegrityError:
            context['message'] = "you cannot modify to an already existing manufacturer"
            context['redirect_url'] = "/manufac/"
            render_template('manufac/message.html', **context)
        return redirect('/manufac/')


@manufac_blueprint.route('/edit/<manufac_name>', methods=['GET', 'POST'])
@login_required
def manufac_edit(manufac_name):
    context = base_context()

    m = Manufacturer.query.get(manufac_name)
    context['manufac_name'] = manufac_name
    return render_template('manufac/edit.html', **context)

# api
@manufac_blueprint.route("/check/<manufac_name>", methods=["GET"])
@login_required
def check(manufac_name):
    has_manufac = Manufacturer.manufacturer_exists(manufac_name)
    return jsonify({"exists":has_manufac})
