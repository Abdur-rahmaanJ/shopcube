"""
This file email.py contains functions for sending
text and html rendered emails asynchronously
"""

from flask_mailman import EmailMultiAlternatives
from flask import render_template
from threading import Thread
from flask import current_app


def _send_email_helper(app, msg):
    """
    Helper function used for sending email message

    Args:
        app (Flask): The flask app object
        msg (flask-mailman email object): any email/messsage object
            defined for flask-mailman. Example EmailMessage
    """
    with app.app_context():
        if (
            "MAIL_USERNAME" not in current_app.config
            or "MAIL_PASSWORD" not in current_app.config
            or current_app.config["MAIL_USERNAME"] is None
            or current_app.config["MAIL_PASSWORD"] is None
        ):
            print(
                "\nShopyo Error: MAIL_USERNAME, and/or MAIL_PASSWORD"
                " not configured\n"
            )
            return

        msg.send()


def send_async_email(to, subject, template, from_email=None, **kwargs):
    """
    Sends email anachronously i.e the function is non blocking.
    Assume email template is valid i.e it can be rendered using
    flask' render_template function and both .html and .txt
    email template files exits

    Args:
        to (String): recipient of the email
        subject (String): subject of the email
        template (String): template file path to be used in email body
        from_email (String, optional): sender of the email. If not set
            MAIL_DEFAULT_SENDER is used from config.
    """

    if from_email is None:
        if (
            "MAIL_DEFAULT_SENDER" not in current_app.config
            or current_app.config["MAIL_DEFAULT_SENDER"] is None
        ):
            print("\nShopyo Error: MAIL_DEFAULT_SENDER not configured\n")
            return

        from_email = current_app.config["MAIL_DEFAULT_SENDER"]

    app = current_app._get_current_object()
    template_txt = render_template(f"{template}.txt", **kwargs)
    template_html = render_template(f"{template}.html", **kwargs)

    msg = EmailMultiAlternatives(
        subject=subject,
        body=template_txt,
        from_email=from_email,
        to=[to],
    )
    msg.attach_alternative(template_html, "text/html")

    thr = Thread(target=_send_email_helper, args=[app, msg])
    thr.start()
    return thr
