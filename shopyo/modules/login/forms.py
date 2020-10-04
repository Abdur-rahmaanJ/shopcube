from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    username = StringField(
        'name', [DataRequired()], render_kw={
            "class": "form-control", "autocomplete": "off"
            })
    password = PasswordField('Password', [DataRequired()],
                             render_kw={"class": "form-control",
                                        "autocomplete": "off"})
    submit = SubmitField('Login', [DataRequired()],
                         render_kw={"class": "btn btn-info"})
