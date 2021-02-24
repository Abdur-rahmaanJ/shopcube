"""
This file (test_email.py) contains the unit tests for
functions defined in email.py which is used for sending
user email confirmation
"""
import pytest
from flask_mailman import EmailMessage

from modules.box__default.auth.email import _send_email_helper
from modules.box__default.auth.email import send_async_email
from modules.box__default.auth.models import User


@pytest.mark.parametrize(
    "email_config",
    [("MAIL_DEFAULT_SENDER", "remove"), ("MAIL_DEFAULT_SENDER", None)],
    indirect=True,
)
def test_send_email_with_no_default_sender(capfd, email_config):
    user = User.create(email="test@gmail.com", password="pass")
    token = "sometoken"
    template = "auth/emails/activate_user"
    subject = "Please confirm your email"
    context = {"token": token, "user": user}
    send_async_email(user.email, subject, template, **context)
    captured = capfd.readouterr()

    assert "Shopyo Error: MAIL_DEFAULT_SENDER not configured" in captured.out


@pytest.mark.parametrize(
    "email_config",
    [
        ("MAIL_USERNAME", "remove"),
        ("MAIL_PASSWORD", "remove"),
        ("MAIL_USERNAME", None),
        ("MAIL_PASSWORD", None),
    ],
    indirect=True,
)
def test_send_email_with_no_username_or_password_set(capfd, email_config):
    user = User.create(email="test@gmail.com", password="pass")
    token = "sometoken"
    template = "auth/emails/activate_user"
    subject = "Please confirm your email"
    context = {"token": token, "user": user}
    thread = send_async_email(user.email, subject, template, **context)
    thread.join()
    captured = capfd.readouterr()

    assert (
        "Shopyo Error: MAIL_USERNAME, and/or MAIL_PASSWORD not configured"
        in captured.out
    )


def test_send_email_using_template_on_valid_credentials(capfd):
    user = User.create(email="to@gmail.com", password="pass")
    token = "sometoken"
    template = "auth/emails/activate_user"
    subject = "Please confirm your email"
    from_email = "from@gmail.com"
    context = {"token": token, "user": user}
    thread = send_async_email(
        user.email, subject, template, from_email=from_email, **context
    )
    thread.join()
    captured = capfd.readouterr()

    assert "Please confirm your email" in captured.out
    assert "sometoken" in captured.out
    assert "to@gmail.com" in captured.out
    assert "from@gmail.com" in captured.out
    assert "Welcome to Shopyo" in captured.out
    assert "To confirm your account please click on" in captured.out
    assert "The Shopyo Team" in captured.out


def test_send_using_helper_function(test_client, flask_app, capfd):
    msg = EmailMessage(
        subject="subject of email",
        body="body of email",
        to=["to@test.com"],
        from_email="from@test.com",
    )
    _send_email_helper(flask_app, msg)
    captured = capfd.readouterr()

    assert "to@test.com" in captured.out
    assert "from@test.com" in captured.out
    assert "subject of email" in captured.out
    assert "body of email" in captured.out
