from flask_wtf import FlaskForm
from wtforms import PasswordField
from wtforms import StringField
from wtforms import SubmitField
from wtforms.validators import DataRequired
from wtforms.validators import Optional
from wtforms.fields.html5 import EmailField
from wtforms.validators import Email
from wtforms.fields.html5 import IntegerField
from wtforms.fields import SelectField
from wtforms import TextAreaField


class CheckoutForm(FlaskForm):
    default_first_name = StringField(
        "First Name",
        [DataRequired()],
        render_kw={"class": "form-control", "autocomplete": "off"},
    )
    default_last_name = StringField(
        "Last Name",
        [DataRequired()],
        render_kw={"class": "form-control", "autocomplete": "off"},
    )
    default_country = StringField(
        "Country",
        [DataRequired()],
        render_kw={"class": "form-control", "autocomplete": "off"},
    )
    default_street = StringField(
        "Street",
        [DataRequired()],
        render_kw={"class": "form-control", "autocomplete": "off"},
    )
    default_town_city = StringField(
        "Town / City",
        [DataRequired()],
        render_kw={"class": "form-control", "autocomplete": "off"},
    )
    default_phone = StringField(
        "Phone",
        [DataRequired()],
        render_kw={"class": "form-control", "autocomplete": "off"},
    )
    default_order_notes =  TextAreaField(
        'Text', 
        [optional()], 
        render_kw={"rows": 10,
        "class": "form-control", "autocomplete": "off"})


    diff_first_name = StringField(
        "First Name",
        [DataRequired()],
        render_kw={"class": "form-control", "autocomplete": "off"},
    )
    diff_last_name = StringField(
        "Last Name",
        [DataRequired()],
        render_kw={"class": "form-control", "autocomplete": "off"},
    )
    diff_country = StringField(
        "Country",
        [DataRequired()],
        render_kw={"class": "form-control", "autocomplete": "off"},
    )
    diff_street = StringField(
        "Street",
        [DataRequired()],
        render_kw={"class": "form-control", "autocomplete": "off"},
    )
    diff_town_city = StringField(
        "Town / City",
        [DataRequired()],
        render_kw={"class": "form-control", "autocomplete": "off"},
    )
    diff_phone = StringField(
        "Phone",
        [DataRequired()],
        render_kw={"class": "form-control", "autocomplete": "off"},
    )
    diff_order_notes =  TextAreaField(
        'Text', 
        [optional()], 
        render_kw={"rows": 10,
        "class": "form-control", "autocomplete": "off"})

    coupon = StringField(
        "Coupon",
        [DataRequired()],
        render_kw={"class": "form-control", "autocomplete": "off"},
    )


    diffAddress = BooleanField('Diff address?',
        render_kw={"class": "form-check-input", 'value': 'diffAddress'})
    applyCoupon = BooleanField('Coupon',
        render_kw={"class": "form-check-input", 'value': 'applyCoupon'})
