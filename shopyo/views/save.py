from flask import (
    Blueprint, render_template, request, redirect
)
from flask_login import login_required, current_user


from models import Appointments
from app import db
from settings import get_value

import requests

save_blueprint = Blueprint('save', __name__, url_prefix='/save')


@save_blueprint.route("/")
@login_required
def save_main():
    def has_internet():
        url='http://www.google.com/'
        timeout=5
        try:
            _ = requests.get(url, timeout=timeout)
            return True
        except requests.ConnectionError:
            print("İnternet bağlantısı yok.")
        return False
    return render_template('save/index.html',
                            has_internet = has_internet(),
                            OUR_APP_NAME=get_value('OUR_APP_NAME'), 
                            SECTION_NAME=get_value('SECTION_NAME')
                        )