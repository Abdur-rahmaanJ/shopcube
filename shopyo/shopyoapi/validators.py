import re

from wtforms.validators import ValidationError

# https://wtforms.readthedocs.io/en/2.3.x/validators/


def is_empty_str(string):
    return string.strip() == ""


def is_valid_slug(text):
    # from validators package
    slug_regex = re.compile(r"^[-a-zA-Z0-9_]+$")
    return slug_regex.match(text)


def verify_slug(form, field):

    if not is_valid_slug(field.data):
        raise ValidationError(
            "Slugs can only contain alphabets, numbers and hyphens (-). eg. good-day-1"
        )


def require_if_default_address(form, field):

    if form.diffAddress.data == False:
        if is_empty_str(field.data):
            raise ValidationError("{} cannot be empty!".format(field.label))


def require_if_diff_address(form, field):
    if form.diffAddress.data == True:
        if is_empty_str(field.data):
            raise ValidationError("{} cannot be empty!".format(field.label))


def require_if_apply_coupon(form, field):

    if form.applyCoupon.data == True:
        if is_empty_str(field.data):
            raise ValidationError("{} cannot be empty!".format(field.label))


def require_if_create_account(form, field):

    if form.createAccount.data == True:
        if is_empty_str(field.data):
            raise ValidationError("{} cannot be empty!".format(field.label))
