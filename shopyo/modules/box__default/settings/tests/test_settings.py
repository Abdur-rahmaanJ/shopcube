"""
This file (test_settings.py) contains the functional tests for
the `settings` blueprint.

These tests use GETs and POSTs to different endpoints to check
for the proper behavior of the `settings` blueprint.
"""

import os
import json
from flask import request
from flask import url_for
import pytest
from modules.box__default.settings.models import Settings


dirpath = os.path.dirname(os.path.abspath(__file__))
module_path = os.path.dirname(dirpath)

module_info = None

with open(os.path.join(module_path, "info.json")) as f:
    module_info = json.load(f)


class TestSettingsInvalidAuth:
    """
    Test all settings routes
    """

    routes_get = ["/", "/edit/<settings_name>", "/update"]

    routes_post = ["/edit/<settings_name>", "/update"]

    @pytest.mark.parametrize("route", routes_get)
    def test_redirect_if_not_logged_in_get(self, test_client, route, auth):
        auth.logout()
        response = test_client.get(
            f"{module_info['url_prefix']}{route}", follow_redirects=True
        )

        assert response.status_code == 200
        assert request.path == url_for("auth.login")

    @pytest.mark.parametrize("route", routes_post)
    def test_redirect_if_not_logged_in_post(self, test_client, route, auth):
        auth.logout()
        response = test_client.post(
            f"{module_info['url_prefix']}{route}", follow_redirects=True
        )

        assert response.status_code == 200
        assert request.path == url_for("auth.login")


@pytest.mark.usefixtures("login_admin_user")
class TestSettingsAPI:
    def test_settings_main(self, test_client):

        response = test_client.get(f"{module_info['url_prefix']}/")
        assert response.status_code == 200
        assert b"APP_NAME" in response.data
        assert b"SECTION_NAME" in response.data
        assert b"ACTIVE_FRONT_THEME" in response.data
        assert b"SECTION_ITEMS" in response.data
        assert b"CURRENCY" in response.data

    @pytest.mark.parametrize(
        "setting",
        [
            "APP_NAME",
            "SECTION_NAME",
            "SECTION_ITEMS",
            "ACTIVE_FRONT_THEME",
            "SECTION_ITEMS",
            "CURRENCY",
        ],
    )
    def test_settings_edit(self, test_client, setting):

        response = test_client.get(
            f"{module_info['url_prefix']}/edit/{setting}"
        )
        assert response.status_code == 200

    def test_settings_update(self, test_client):

        response = test_client.post(
            f"{module_info['url_prefix']}/update",
            data=dict(
                settings_name="APP_NAME",
                settings_value="TEST-APP-NAME",
                follow_redirects=True,
            ),
        )

        setting = Settings.query.get("APP_NAME")
        assert response.status_code == 200
        assert setting is not None
        assert setting.value == "TEST-APP-NAME"
