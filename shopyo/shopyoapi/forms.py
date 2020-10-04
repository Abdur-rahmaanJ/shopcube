from shopyoapi.html import notify_warning
from flask import flash

def flash_errors(form):
    """Flashes form errors"""
    for field, errors in form.errors.items():
        for error in errors:
            error_msg = u"Error in the %s field - %s" % (
                getattr(form, field).label.text,
                error
            )
            flash(notify_warning(error_msg))