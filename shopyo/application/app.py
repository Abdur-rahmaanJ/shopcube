from models import app
from flask import (
    Flask, redirect, url_for, render_template
    )

from views.manufac  import manufac_blueprint
from views.products import prod_blueprint
from views.settings_modif import settings_blueprint
from views.patient import patient_blueprint
from views.appointment import appointment_blueprint

app.register_blueprint(manufac_blueprint)
app.register_blueprint(prod_blueprint)
app.register_blueprint(settings_blueprint)
app.register_blueprint(patient_blueprint)
app.register_blueprint(appointment_blueprint)

@app.route('/')
def index():
    return redirect('/manufac/')

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1')