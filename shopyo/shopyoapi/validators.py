import re

from wtforms.validators import ValidationError

# https://wtforms.readthedocs.io/en/2.3.x/validators/


def is_valid_slug(text):
    # from validators package
    slug_regex = re.compile(r"^[-a-zA-Z0-9_]+$")
    return slug_regex.match(text)


def verify_slug(form, field):

    if not is_valid_slug(field.data):
        raise ValidationError(
            "Slugs can only contain alphabets, numbers and hyphens (-). eg. good-day-1"
        )
