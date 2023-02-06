from flask_wtf import FlaskForm
from wtforms import EmailField
from wtforms import StringField
from wtforms import TextAreaField
from wtforms.validators import DataRequired

# from wtforms.validators import Length


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
