from flask_wtf import FlaskForm
from wtforms import PasswordField
from wtforms import StringField
from wtforms import SubmitField
from wtforms import TextAreaField
from wtforms.fields import SelectField

# from wtforms.fields.html5 import EmailField
from wtforms.fields.html5 import IntegerField
from wtforms.validators import DataRequired

# from wtforms.validators import Email
# from wtforms.validators import Optional


class DeliveryOptionForm(FlaskForm):
    option = StringField(
        "Option",
        [DataRequired()],
        render_kw={"class": "form-control", "autocomplete": "off"},
    )
    price = IntegerField(
        "Price",
        [DataRequired()],
        render_kw={"class": "form-control", "autocomplete": "off"},
    )


class PaymentOptionForm(FlaskForm):
    name = StringField(
        "Option",
        [DataRequired()],
        render_kw={"class": "form-control", "autocomplete": "off"},
    )
    text = TextAreaField(
        "Text",
        [DataRequired()],
        render_kw={"rows": 10, "class": "form-control", "autocomplete": "off"},
    )


class CouponForm(FlaskForm):
    string = StringField(
        "String",
        [DataRequired()],
        render_kw={"class": "form-control", "autocomplete": "off"},
    )
    type = SelectField(
        "Type",
        choices=[("percentage", "percentage"), ("value", "value")],
        validators=[DataRequired()],
        render_kw={"class": "form-control"},
    )
    value = IntegerField(
        "Value",
        [DataRequired()],
        render_kw={"class": "form-control", "autocomplete": "off"},
    )


class CurrencyForm(FlaskForm):
    currency = SelectField(
        "Currency",
        validators=[DataRequired()],
        render_kw={"class": "form-control"},
    )
