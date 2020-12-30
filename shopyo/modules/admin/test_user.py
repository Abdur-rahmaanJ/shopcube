from flask import url_for, request
import pytest


def test_new_user(new_user):
    """
    GIVEN a User model
    WHEN a new User is created
    THEN check the email, password, admin privilege
    """
    assert new_user.email == "admin3@domain.com"
    assert new_user.password != "pass"
    assert not new_user.is_admin


@pytest.mark.order('first')
def test_home_page(test_client, init_database):
    """
    GIVEN a Flask application configured for testing and an
    intitail testing database,
    WHEN the '/' page is requested (GET)
    THEN check that the response is valid
    """
    # '/' redirects to /shop/home
    response = test_client.get("/",  follow_redirects=True)
    assert response.status_code == 200


@pytest.mark.order('second')
def test_valid_login_logout(test_client):
    """
    GIVEN a Flask application configured for testing,
    WHEN the logging in and loggoing out from the app
    THEN check that the response is valid for each case
    """

    # Login to the app
    response = test_client.post(
        url_for("login.login"),
        data=dict(email="admin1@domain.com", password="pass"),
        follow_redirects=True,
    )

    # Check if login was successful
    assert response.status_code == 200
    assert b"Control panel" in response.data
    assert b"Notif test" in response.data

    # Check response is redirect to login page
    response = test_client.get(url_for("login.logout"), follow_redirects=True)
    assert response.status_code == 200
    assert request.path == url_for('login.login')
    assert b"Successfully logged out" in response.data
