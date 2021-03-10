import re

from wtforms.validators import ValidationError

# https://wtforms.readthedocs.io/en/2.3.x/validators/


def is_empty_str(string):
    return string.strip() == ""


def is_valid_slug(text):
    # from validators package
    slug_regex = re.compile(r"^[-a-zA-Z0-9_]+$")
    return slug_regex.match(text)


def is_valid_url(url):
    protocol = r'^((?:http|ftp)s?://)?'
    domain = (r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?'
              + r'|localhost)')
    ipv4 = (r'(?:25[0-5]|2[0-4]\d|[0-1]?\d?\d)(?:\.(?:25[0-5]|2[0-4]\d|'
            + r'[0-1]?\d?\d)){3}')
    ipv6 = r'([a-f0-9:]+:+)+[a-f0-9]+'
    port = r'(?::\d+)?(?:/?|[/?]\S+)$'
    url_regex = re.compile(protocol + domain + "|" + ipv4 + "|" + ipv6
                           + port, re.IGNORECASE)
    return url_regex.match(url) is not None


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
