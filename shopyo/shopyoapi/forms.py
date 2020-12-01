from flask import flash

from shopyoapi.html import notify_warning


def flash_errors(form):
    """
    Auto flash errors from WKHtml forms
    Reqwires base module or similar notification
    mechanism

    Parameters
    ----------
    form: WKHtml form

    Returns
    -------
    None
    """
    for field, errors in form.errors.items():
        for error in errors:
            error_msg = u"Error in the %s field - %s" % (
                getattr(form, field).label.text,
                error,
            )
            flash(notify_warning(error_msg))
