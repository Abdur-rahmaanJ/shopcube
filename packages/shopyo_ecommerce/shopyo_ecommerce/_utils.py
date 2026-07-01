import re

from shopyo.api.validators import is_empty_str
from shopyo_settings.helpers import get_setting
from iso4217parse import by_alpha3


def get_currency_symbol():
    code = get_setting("CURRENCY") or "USD"
    currency = by_alpha3(code)
    return currency.symbols[0] if currency else code
from shopyo.api.file import unique_filename
from werkzeug.utils import secure_filename
from wtforms.validators import ValidationError


def is_safe_path_component(component):
    if not component:
        return False
    return bool(re.match(r"^[a-zA-Z0-9_.\-]+$", component))


def unique_sec_filename(filename):
    return unique_filename(secure_filename(filename))


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
