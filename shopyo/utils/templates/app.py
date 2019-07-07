from flask import (
    Flask, redirect, url_for, render_template
    )
from models import app

from views.manufac  import manufac_blueprint
from views.products import prod_blueprint
from views.people import person_blueprint
from views.settings_modif import settings_blueprint
{{IMPORTS}}

app.register_blueprint(manufac_blueprint)
app.register_blueprint(prod_blueprint)
app.register_blueprint(person_blueprint)
app.register_blueprint(settings_blueprint)
{{REGISTER_BLUEPRINTS}}

@app.route('/')
def index():
    return redirect('/manufac/')

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1')
