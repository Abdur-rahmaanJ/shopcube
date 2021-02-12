"""
This file (test_login.py) contains the functional tests for
the `login` blueprint.

These tests use GETs and POSTs to different endpoints to check
for the proper behavior of the `login` blueprint.
"""
from flask import url_for
from flask import request


def test_valid_login_logout(test_client):
    """
    GIVEN a Flask application configured for testing,
    WHEN the logging in and loggoing out from the app
    THEN check that the response is valid for each case
    """
    # Login to the app
    response = test_client.post(
        url_for("auth.login"),
        data=dict(email="admin1@domain.com", password="pass"),
        follow_redirects=True,
    )

    # Check if login was successful
    assert response.status_code == 200
    assert b"Control panel" in response.data
    assert b"Notif test" in response.data

    # Check response is redirect to login page
    response = test_client.get(url_for("auth.logout"), follow_redirects=True)
    assert response.status_code == 200
    assert request.path == url_for("auth.login")
    assert b"Successfully logged out" in response.data
