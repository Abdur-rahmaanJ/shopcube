from flask_wtf import FlaskForm
from wtforms import PasswordField
from wtforms import StringField
from wtforms import TextAreaField
from wtforms.fields import BooleanField
from wtforms.fields import EmailField
from wtforms.fields import SelectField

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


from flask_wtf import FlaskForm
from wtforms import PasswordField
from wtforms.fields import EmailField
from wtforms.validators import DataRequired
from wtforms.validators import Email
from wtforms.validators import EqualTo
from wtforms.validators import InputRequired
from wtforms.validators import Length
from wtforms.validators import ValidationError

from modules.box__default.auth.models import User


class LoginForm(FlaskForm):
    email = EmailField(
        "email",
        [DataRequired(), Email(message=("Not a valid email address."))],
        render_kw={"class": "form-control", "autocomplete": "off"},
    )
    password = PasswordField(
        "Password",
        [DataRequired()],
        render_kw={"class": "form-control", "autocomplete": "off"},
    )


class RegistrationForm(FlaskForm):
    """Registration Form"""

    email = EmailField(
        "email_label",
        [DataRequired(), Email(message=("Not a valid email address."))],
    )

    password = PasswordField(
        "New Password",
        validators=[
            InputRequired("Password is required"),
            Length(
                min=6,
                max=25,
                message="Password must be between 6 and 25 characters",
            ),
            EqualTo("confirm", message="Passwords must match"),
        ],
    )
    confirm = PasswordField(
        "Repeat Password",
    )

    def validate_email(self, field):
        """
        Inline validator for email. Checks to see if a user object with
        entered email already present in the database

        Args:
            field : The form field that contains email data.

        Raises:
            ValidationError: if the username entered in the field is already
            in the database
        """
        user = User.query.filter_by(email=field.data).scalar()

        if user is not None:
            raise ValidationError(f"email '{field.data}' is already in use.")


class RegisterCustomerForm(FlaskForm):
    email = EmailField(
        "Email",
        [DataRequired(), Email(message=("Not a valid email address."))],
        render_kw={"class": "form-control", "autocomplete": "off"},
    )
    password = PasswordField(
        "Password",
        [DataRequired()],
        render_kw={"class": "form-control", "autocomplete": "off"},
    )
    reconfirm_password = PasswordField(
        "Password",
        [DataRequired()],
        render_kw={"class": "form-control", "autocomplete": "off"},
    )
