from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms import TextField
from wtforms import SelectField
from wtforms.fields.html5 import EmailField
from wtforms import SubmitField
from wtforms import PasswordField
from wtforms.validators import DataRequired

# from wtforms.validators import Length
from wtforms import TextAreaField


class ContactForm(FlaskForm):
    name = StringField(
        "Name",
        [DataRequired()],
        render_kw={"class": "form-control", "autocomplete": "off"},
    )
    email = EmailField(
        "Email",
        [DataRequired()],
        render_kw={"class": "form-control", "autocomplete": "off"},
    )
    message = TextAreaField(
        "Message",
        [DataRequired()],
        render_kw={"class": "form-control", "rows": "20", "autocomplete": "off"},
    )
