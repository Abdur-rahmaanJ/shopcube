from flask_mailman import EmailMultiAlternatives
from flask import render_template
from threading import Thread
from flask import current_app


def send_async_email(app, msg):
    with app.app_context():

        if any(
            (
                app.config["MAIL_USERNAME"] is None,
                app.config["MAIL_PASSWORD"] is None,
                app.config['MAIL_DEFAULT_SENDER'] is None
            )
        ):
            print("\n---Shopyo-LOG: at send_async_email()---")
            print("Error: MAIL_USERNAME, MAIL_PASSWORD, or ")
            print("MAIL_DEFAULT_SENDER not configured\n")
            return

        try:
            msg.send()
        except Exception as e:
            print("---Shopyo-LOG: at send_async_email()---")
            print(f"Unable to send confirmation email: {e}")


def send_email(recipients, subject, template, **kwargs):
    app = current_app._get_current_object()
    template_txt = render_template(f"{template}.txt", **kwargs)
    template_html = render_template(f"{template}.html", **kwargs)
    msg = EmailMultiAlternatives(
        subject=subject,
        body=template_txt,
        from_email=current_app.config['MAIL_DEFAULT_SENDER'],
        to=[recipients],
    )
    msg.attach_alternative(template_html, "text/html")
    thr = Thread(target=send_async_email, args=[app, msg])
    thr.start()
