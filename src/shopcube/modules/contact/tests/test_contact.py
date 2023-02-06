"""
This file (test_contact.py) contains the functional tests for the
`contact` blueprint.

These tests use GETs and POSTs to different endpoints to check for
the proper behavior of the `contact` blueprint.
"""
from flask import request
from flask import url_for


def test_contact_page(test_client):
    """
    GIVEN a Flask application configured for testing,
    WHEN the /contact page is requested (GET)
    THEN check that the response is valid
    """
    response = test_client.get("/contact/")
    assert response.status_code == 200
    assert b"Name" in response.data
    assert b"Email" in response.data
    assert b"Message" in response.data
    assert b"Submit" in response.data


def test_contact_dashboard(test_client):
    """
    GIVEN a Flask application configured for testing,
    WHEN the /contact/dashboard page is requested (GET)
    THEN check that the response is valid
    """
    # Logout and try to access the contact dashboard. It should redirect
    response = test_client.get(url_for("auth.logout"), follow_redirects=True)
    print(request.path)
    assert response.status_code == 200
    assert request.path == url_for("auth.login")

    # check request to contact correctly redirects to login page
    response = test_client.get("/contact/dashboard", follow_redirects=True)
    assert request.path == url_for("auth.login")

    # Login and try to access the contact dashboard. It should return OK
    response = test_client.post(
        url_for("auth.login"),
        data=dict(email="admin1@domain.com", password="pass"),
        follow_redirects=True,
    )

    # check if successfully logged in
    assert response.status_code == 200

    # check response is valid
    response = test_client.get(url_for("contact.dashboard"))
    assert response.status_code == 200
    assert b"Contact dashboard" in response.data
    assert b"Name" in response.data
    assert b"Mail" in response.data
    assert b"Date" in response.data
    assert b"Info" in response.data
    assert b"View message" not in response.data


def test_contact_validate_msg(test_client):
    """
    GIVEN a Flask application configured for testing,
    WHEN POST request is made contact validate page
    THEN check that the response is valid and that
    the new validated message appears on contact dashboard
    """
    # GET request should fail for validate message
    # Currently test is uncommented since no return statement for
    # validate_message for GET
    # UNCOMMENT BELOW CODE AFTER FIXING validate_message
    # response = test_client.get(url_for("contact.validate_message"))
    # assert response.status_code != 200

    # add a message
    response = test_client.post(
        url_for("contact.validate_message"),
        data=dict(name="User1", email="user1@gmail.com", message="User1 Message"),
        follow_redirects=True,
    )
    assert response.status_code == 200

    # check if message was added successfully
    response = test_client.get(url_for("contact.dashboard", page=1))
    assert response.status_code == 200
    assert b"Contact dashboard" in response.data
    assert b"User1" in response.data
    assert b"user1@gmail.com" in response.data
    assert b"User1 Message" in response.data
    assert b"View message" in response.data

    # change contact page and make sure the message is not there
    response = test_client.get(url_for("contact.dashboard", page=2))
    assert response.status_code == 200
    assert b"User1" not in response.data
    assert b"user1@gmail.com" not in response.data
    assert b"User1 Message" not in response.data
    assert b"View message" not in response.data
