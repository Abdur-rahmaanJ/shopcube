#from models import db
from addon import db, ma, login_manager
from flask import (
    Flask, redirect, url_for, render_template
    )

from flask_sqlalchemy import SQLAlchemy
from functools import wraps

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'qow32ijjdkc756osk5dmck'  # Need a generator

#db = SQLAlchemy(app)
db.init_app(app)
ma.init_app(app)
login_manager.init_app(app)

from views.manufac import manufac_blueprint
from views.products import prod_blueprint
from views.settings_modif import settings_blueprint
from views.appointment import appointment_blueprint
from views.people import people_blueprint
from views.admin_modif import admin_blueprint
from views.login import login_blueprint
from views.save import save_blueprint


app.register_blueprint(manufac_blueprint)
app.register_blueprint(prod_blueprint)
app.register_blueprint(settings_blueprint)
app.register_blueprint(appointment_blueprint)
app.register_blueprint(people_blueprint)
app.register_blueprint(admin_blueprint)
app.register_blueprint(login_blueprint)
app.register_blueprint(save_blueprint)

@app.route('/')
def index():
    return redirect('/manufac/')

if __name__ == '__main__':
    
    app.run()
