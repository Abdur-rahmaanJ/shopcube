from flask_wtf import FlaskForm
from wtforms import PasswordField
from wtforms import StringField
from wtforms import SubmitField
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    username = StringField(
        "name",
        [DataRequired()],
        render_kw={"class": "form-control", "autocomplete": "off"},
    )
    password = PasswordField(
        "Password",
        [DataRequired()],
        render_kw={"class": "form-control", "autocomplete": "off"},
    )
