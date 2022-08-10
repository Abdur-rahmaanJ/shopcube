from flask_wtf import FlaskForm
from wtforms import PasswordField
from wtforms import StringField
from wtforms import TextAreaField
from wtforms.fields import BooleanField
from wtforms.fields import SelectField
from wtforms.fields import EmailField

# from wtforms.fields import IntegerField
# from wtforms.validators import DataRequired
# from wtforms.validators import Email
from wtforms.validators import Optional

from utils.validators import require_if_apply_coupon
from utils.validators import require_if_create_account
from utils.validators import require_if_default_address
from utils.validators import require_if_diff_address


class CheckoutForm(FlaskForm):

    diffAddress = BooleanField(
        "Ship to a different address than the default one?",
        render_kw={
            "class": "form-check-input",
            "value": "diffAddress",
            "id": "diffAddress",
        },
    )
    applyCoupon = BooleanField(
        "Apply Coupon",
        render_kw={
            "class": "form-check-input",
            "value": "applyCoupon",
            "id": "applyCoupon",
        },
    )
    createAccount = BooleanField(
        "Create Account?",
        render_kw={
            "class": "form-check-input",
            "value": "createAccount",
            "id": "createAccount",
        },
    )

    default_first_name = StringField(
        "First Name",
        [require_if_default_address],
        render_kw={"class": "form-control", "autocomplete": "off"},
    )
    default_last_name = StringField(
        "Last Name",
        [require_if_default_address],
        render_kw={"class": "form-control", "autocomplete": "off"},
    )
    default_country = SelectField(
        "Country",
        render_kw={"class": "form-control", "autocomplete": "off"},
    )
    default_street = StringField(
        "Street",
        [require_if_default_address],
        render_kw={"class": "form-control", "autocomplete": "off"},
    )
    default_town_city = StringField(
        "Town / City",
        [require_if_default_address],
        render_kw={"class": "form-control", "autocomplete": "off"},
    )
    default_phone = StringField(
        "Phone",
        [require_if_default_address],
        render_kw={"class": "form-control", "autocomplete": "off"},
    )
    default_email = EmailField(
        "Email",
        [require_if_default_address],
        render_kw={"class": "form-control", "autocomplete": "off"},
    )
    default_order_notes = TextAreaField(
        "Order Notes (optional)",
        [Optional()],
        render_kw={"rows": 10, "class": "form-control", "autocomplete": "off"},
    )

    diff_first_name = StringField(
        "First Name",
        [require_if_diff_address],
        render_kw={"class": "form-control", "autocomplete": "off"},
    )
    diff_last_name = StringField(
        "Last Name",
        [require_if_diff_address],
        render_kw={"class": "form-control", "autocomplete": "off"},
    )
    diff_country = SelectField(
        "Country",
        render_kw={
            "class": "form-control",
            "autocomplete": "off",
        },
    )
    diff_street = StringField(
        "Street",
        [require_if_diff_address],
        render_kw={"class": "form-control", "autocomplete": "off"},
    )
    diff_town_city = StringField(
        "Town / City",
        [require_if_diff_address],
        render_kw={"class": "form-control", "autocomplete": "off"},
    )
    diff_phone = StringField(
        "Phone",
        [require_if_diff_address],
        render_kw={"class": "form-control", "autocomplete": "off"},
    )
    diff_email = EmailField(
        "Email",
        [require_if_diff_address],
        render_kw={"class": "form-control", "autocomplete": "off"},
    )
    diff_order_notes = TextAreaField(
        "Order Notes (optional)",
        [Optional()],
        render_kw={"rows": 10, "class": "form-control", "autocomplete": "off"},
    )

    coupon = StringField(
        "Coupon",
        [require_if_apply_coupon],
        render_kw={"class": "form-control", "autocomplete": "off"},
    )

    password = PasswordField(
        "Coupon",
        [require_if_create_account],
        render_kw={"class": "form-control", "autocomplete": "off"},
    )
