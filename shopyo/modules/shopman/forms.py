from flask_wtf import FlaskForm
from wtforms import PasswordField
from wtforms import StringField
from wtforms import SubmitField
from wtforms.validators import DataRequired
from wtforms.fields.html5 import EmailField
from wtforms.validators import Email
from wtforms.fields.html5 import IntegerField

class DeliveryOptionForm(FlaskForm):
    option = StringField(
        "Option Text",
        [DataRequired()],
        render_kw={"class": "form-control", "autocomplete": "off"},
    )
    price = IntegerField(
        "Price",
        [DataRequired()],
        render_kw={"class": "form-control", "autocomplete": "off"},
    )
