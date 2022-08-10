from flask_wtf import FlaskForm
from wtforms import PasswordField
from wtforms.fields import EmailField
from wtforms.validators import DataRequired
from wtforms.validators import Email
from wtforms.validators import InputRequired
from wtforms.validators import Length
from wtforms.validators import EqualTo
from wtforms.validators import ValidationError
from modules.box__default.admin.models import User


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
    """ Registration Form """

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
