"""
This file (test_auth_functional.py) contains the functional tests for
the `auth` blueprint.

These tests use GETs and POSTs to different endpoints to check
for the proper behavior of the `auth` module
"""
from flask import url_for
from flask import request
import pytest
import os
import json
import threading
from modules.box__default.auth.models import User
from flask_login import current_user

dirpath = os.path.dirname(os.path.abspath(__file__))
module_path = os.path.dirname(dirpath)

module_info = None

with open(os.path.join(module_path, "info.json")) as f:
    module_info = json.load(f)


class TestAuthInvalidAccess:
    """
    Test all auth routes for correct user authentication
    """

    routes_get = [
        "/confirm/<token>",
        "/resend",
        "/unconfirmed",
    ]

    @pytest.mark.parametrize("route", routes_get)
    def test_redirect_if_not_logged_in_get(self, test_client, route, auth):
        auth.logout()
        response = test_client.get(
            f"{module_info['url_prefix']}{route}", follow_redirects=True
        )

        assert response.status_code == 200
        assert request.path == url_for("auth.login")


class TestAuthEndpoints:
    """
    Test all auth routes' functionalities
    """

    def test_user_registration_page_renders(self, test_client):
        response = test_client.get(f"{module_info['url_prefix']}/register")

        assert response.status_code == 200
        assert b"Email" in response.data
        assert b"Password" in response.data
        assert b"Confirm Password" in response.data
        assert b"Register" in response.data

    def test_user_not_registered_on_invalid_form_submit(self, test_client):
        User.create(email="test@gmail.com", password="pass")
        data = {
            "email": "test@gmail.com",
            "password": "password",
            "confirm": "password",
        }

        response = test_client.post(
            f"{module_info['url_prefix']}/register",
            data=data,
            follow_redirects=True,
        )

        assert response.status_code == 200
        assert request.path == url_for("auth.register")

    def test_user_registration_is_case_insensitive(self, test_client):
        User.create(email="foo@bar.com", password="pass")
        data = {
            "email": "Foo@Bar.com",
            "password": "password",
            "confirm": "password",
        }

        response = test_client.post(
            f"{module_info['url_prefix']}/register",
            data=data,
            follow_redirects=True,
        )

        assert response.status_code == 200
        assert request.path == url_for("auth.register")

    @pytest.mark.parametrize(
        "email_config",
        [
            ("EMAIL_CONFIRMATION_DISABLED", True),
        ],
        indirect=True,
    )
    def test_user_confirmed_if_email_disabled(self, test_client, email_config):
        data = {
            "email": "test@gmail.com",
            "password": "password",
            "confirm": "password",
        }
        response = test_client.post(
            f"{module_info['url_prefix']}/register",
            data=data,
            follow_redirects=True,
        )
        user = User.query.filter(User.email == "test@gmail.com").scalar()

        assert response.status_code == 200
        assert request.path == url_for("dashboard.index")
        assert user.is_email_confirmed is True

    @pytest.mark.parametrize(
        "email_config",
        [
            ("EMAIL_CONFIRMATION_DISABLED", "remove"),
            ("EMAIL_CONFIRMATION_DISABLED", False),
            ("EMAIL_CONFIRMATION_DISABLED", None),
        ],
        indirect=True,
    )
    def test_user_is_registered_on_valid_form_submit(
        self, test_client, capfd, email_config
    ):
        data = {
            "email": "test@gmail.com",
            "password": "password",
            "confirm": "password",
        }
        response = test_client.post(
            f"{module_info['url_prefix']}/register",
            data=data,
            follow_redirects=True,
        )
        # Not very happy with this solution. Need a better
        # way to wait for the email thread to join with main
        # thread before reading the email written to stdout @rehmanis
        while threading.activeCount() > 1:
            pass
        else:
            captured = capfd.readouterr()

        user = User.query.filter(User.email == "test@gmail.com").scalar()

        assert response.status_code == 200
        assert request.path == url_for("auth.unconfirmed")
        assert b"A confirmation email has been sent via email" in response.data
        assert "test@gmail.com" in captured.out
        assert "Welcome to Shopyo" in captured.out
        assert user is not None
        assert user.is_email_confirmed is False

    @pytest.mark.usefixtures("login_non_admin_user")
    def test_user_not_confirmed_for_already_confirmed_user(self, test_client):
        response = test_client.get(
            url_for("auth.confirm", token="sometoken"), follow_redirects=True
        )

        assert response.status_code == 200
        assert request.path == url_for("dashboard.index")
        assert b"Account already confirmed." in response.data

    @pytest.mark.usefixtures("login_unconfirmed_user")
    def test_user_confirmed_on_valid_token(self, test_client):
        token = current_user.generate_confirmation_token()
        response = test_client.get(
            url_for("auth.confirm", token=token), follow_redirects=True
        )

        assert response.status_code == 200
        assert request.path == url_for("dashboard.index")
        assert b"You have confirmed your account. Thanks!" in response.data
        assert current_user.is_email_confirmed is True

    @pytest.mark.usefixtures("login_unconfirmed_user")
    def test_no_confirm_sent_for_invalid_token(self, test_client):
        token = current_user.generate_confirmation_token() + "extra"
        response = test_client.get(
            url_for("auth.confirm", token=token), follow_redirects=True
        )

        assert response.status_code == 200
        assert request.path == url_for("auth.unconfirmed")
        assert b"The confirmation link is invalid/expired." in response.data

    @pytest.mark.usefixtures("login_non_admin_user")
    def test_do_not_allow_email_resend_for_confirmed(self, test_client):
        response = test_client.get(
            url_for("auth.resend"), follow_redirects=True
        )

        assert response.status_code == 200
        assert request.path == url_for("dashboard.index")

    @pytest.mark.usefixtures("login_unconfirmed_user")
    def test_valid_resend_email_confirmation(self, test_client, capfd):
        response = test_client.get(
            url_for("auth.resend"), follow_redirects=True
        )

        # Not very happy with this solution. Need a better
        # way to wait for the email thread to join with main
        # thread before reading the email written to stdout @rehmanis
        while threading.activeCount() > 1:
            pass
        else:
            captured = capfd.readouterr()

        assert response.status_code == 200
        assert current_user.email in captured.out
        assert "Welcome to Shopyo" in captured.out
        assert request.path == url_for("auth.unconfirmed")
        assert b"A new confirmation email has been sent" in response.data

    @pytest.mark.usefixtures("login_non_admin_user")
    def test_confirmed_user_is_redirected_to_dashboard(self, test_client):
        response = test_client.get(
            url_for("auth.unconfirmed"), follow_redirects=True
        )

        assert response.status_code == 200
        assert request.path == url_for("dashboard.index")

    @pytest.mark.usefixtures("login_unconfirmed_user")
    def test_unconfirmed_page_renders_correctly(self, test_client):
        response = test_client.get(url_for("auth.unconfirmed"))

        assert response.status_code == 200
        assert request.path == url_for("auth.unconfirmed")
        assert b"You have not confirmed your account" in response.data
        assert b"Email confirmation link was sent to" in response.data
        assert current_user.email.encode() in response.data

    def test_login_for_dashboard_renders(self, test_client):
        response = test_client.get(url_for("auth.login"))

        response.status_code == 200
        assert b"Login" in response.data
        assert b"submit" in response.data

    def test_invalid_dashboard_login(self, test_client):
        response = test_client.post(
            url_for("auth.login"),
            data=dict(email="admin1@domain.com", password="wrongpass"),
            follow_redirects=True,
        )

        response.status_code == 200
        assert request.path == url_for("auth.login")
        assert b"please check your user id and password" in response.data

    def test_valid_dashboard_login(self, test_client, non_admin_user):
        response = test_client.post(
            url_for("auth.login"),
            data=dict(email=non_admin_user.email, password="pass"),
            follow_redirects=True,
        )

        assert response.status_code == 200
        assert current_user.email == non_admin_user.email
        assert request.path == url_for("dashboard.index")

    def test_valid_dashboard_login_is_case_insensitive(self, test_client):
        User.create(email="foo@bar.com", password="pass")
        data = {"email": "Foo@Bar.com", "password": "pass"}
        response = test_client.post(
            url_for("auth.login"),
            data=data,
            follow_redirects=True,
        )

        assert response.status_code == 200
        assert current_user.email.lower() == data["email"].lower()
        assert request.path == url_for("auth.unconfirmed")

    @pytest.mark.usefixtures("login_non_admin_user")
    def test_current_user_logout(self, test_client):
        response = test_client.get(
            url_for("auth.logout"), follow_redirects=True
        )

        assert response.status_code == 200
        assert request.path == url_for("auth.login")
        assert b"Successfully logged out" in response.data
        assert current_user.is_authenticated is False
