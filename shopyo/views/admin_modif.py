from flask import (
    Blueprint, render_template, request, redirect

    )
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_required, current_user
from models import Users
from app import db
from settings import get_value
from sqlalchemy import exists
from admin import admin_required

# Should maybe change URL?
admin_blueprint = Blueprint('admin', __name__, url_prefix='/admin')


@admin_blueprint.route("/")
@login_required
@admin_required
def user_list():
    return render_template('admin/index.html', users=Users.query.all(),
                           OUR_APP_NAME=get_value('OUR_APP_NAME'),
                           SECTION_NAME=get_value('SECTION_NAME'))


@admin_blueprint.route('/add', methods=['GET', 'POST'])
@login_required
@admin_required
def user_add():
    if request.method == 'POST':
        id = request.form['id']
        name = request.form['name']
        password = request.form['password']
        admin_user = request.form.get('admin_user')
        if admin_user == 'True':
            admin_user = True
        else:
            admin_user = False

        has_user = db.session.query(exists().where(Users.id == id)).scalar()

        if has_user is False:
            new_user = Users(id=id, name=name, admin_user=admin_user)
            new_user.set_hash(password)
            db.session.add(new_user)
            db.session.commit()
            return render_template('admin/add.html',
                                   OUR_APP_NAME=get_value('OUR_APP_NAME'),
                                   SECTION_NAME=get_value('SECTION_NAME'))
    return render_template('admin/add.html',
                           OUR_APP_NAME=get_value('OUR_APP_NAME'),
                           SECTION_NAME=get_value('SECTION_NAME'))


@admin_blueprint.route('/delete/<id>', methods=['GET', 'POST'])
@login_required
@admin_required
def admin_delete(id):
    Users.query.filter(Users.id == id).delete()
    db.session.commit()
    return redirect('/admin')


@admin_blueprint.route('/edit/<id>', methods=['GET', 'POST'])
@login_required
@admin_required
def appointment_edit(id):
    u = Users.query.get(id)
    return render_template('admin/edit.html', id=u.id,
                           name=u.name, password=u.password,
                           admin_user=u.admin_user,
                           OUR_APP_NAME=get_value('OUR_APP_NAME'),
                           SECTION_ITEMS=get_value('SECTION_ITEMS'))


@admin_blueprint.route('/update', methods=['GET', 'POST'])
@login_required
@admin_required
def admin_update():
    id = request.form['id']
    name = request.form['name']
    password = request.form['password']
    admin_user = request.form.get('admin_user')
    if admin_user == 'True':
        admin_user = True
    else:
        admin_user = False
    u = Users.query.get(id)
    u.name = name
    u.set_hash(password)
    u.admin_user = admin_user
    db.session.add(u)
    db.session.commit()
    return redirect('/admin')
