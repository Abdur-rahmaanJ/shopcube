from flask import (
    Blueprint, render_template, request, redirect, url_for, flash

    )
from flask_login import login_required, current_user, login_user, logout_user
from addon import db, login_manager
from views.admin.models import Users
from project_api import base_context


login_blueprint = Blueprint('login', __name__, url_prefix='/login')


@login_blueprint.route('/', methods=['GET', 'POST'])
def login():
    context = base_context()

    if request.method == 'POST':
        user_id = request.form['user_id']
        password = request.form['password']
        user = Users.query.filter_by(id=user_id).first()
        if user is None or not user.check_hash(password):
            flash('please check your user id and password')
            return redirect(url_for('login.login'))
        login_user(user)
        return redirect(url_for('manufac.manufac'))
    return render_template('admin/login.html', **context)


@login_blueprint.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/login')
