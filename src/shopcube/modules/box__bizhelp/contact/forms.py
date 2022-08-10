from flask_wtf import FlaskForm

# from wtforms.validators import Length
from wtforms import StringField
from wtforms import TextAreaField
from wtforms.fields import EmailField
from wtforms.validators import DataRequired


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
        render_kw={
            "class": "form-control",
            "rows": "20",
            "autocomplete": "off",
        },
    )
