from flask import (
    Blueprint, render_template, request, redirect, url_for, flash

    )
from flask_login import login_required, current_user, login_user, logout_user
from models import db, Users
from settings import get_value


login_blueprint = Blueprint('login', __name__, url_prefix='/login')


@login_blueprint.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user_id = request.form['user_id']
        password = request.form['password']
        user = Users.query.filter_by(id=user_id).first()
        if user is None or not user.check_hash(password):
            flash('please check your user id and password')
            return redirect(url_for('login.login'))
        login_user(user)
        return redirect(url_for('manufac.manufac'))
    return render_template('admin/login.html',
                           OUR_APP_NAME=get_value('OUR_APP_NAME'),
                           SECTION_NAME=get_value('SECTION_NAME'))


@login_blueprint.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/login')
