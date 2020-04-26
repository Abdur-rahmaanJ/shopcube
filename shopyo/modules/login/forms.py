from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField


class LoginForm(FlaskForm):
    user_id = StringField('user_id')
    password = PasswordField('password')
