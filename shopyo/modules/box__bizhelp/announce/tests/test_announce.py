"""
This file (test_contact.py) contains the functional tests for the
`contact` blueprint.

These tests use GETs and POSTs to different endpoints to check for
the proper behavior of the `contact` blueprint.
"""
import json
import os

from flask import request
from flask import url_for

from modules.box__bizhelp.announce.models import Announcement

dirpath = os.path.dirname(os.path.abspath(__file__))
module_path = os.path.dirname(dirpath)

module_info = None

with open(os.path.join(module_path, "info.json")) as f:
    module_info = json.load(f)


def test_announce_dashboard(test_client):
    """"""
    response = test_client.get(url_for("auth.logout"), follow_redirects=True)
    print(request.path)
    assert response.status_code == 200
    assert request.path == url_for("auth.login")

    # check request to contact correctly redirects to login page
    response = test_client.get(
        module_info["url_prefix"] + "/dashboard", follow_redirects=True
    )
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
    response = test_client.get(
        url_for(module_info["module_name"] + ".dashboard")
    )
    assert response.status_code == 200
    assert b"New Announcement" in response.data
    assert b"Title" in response.data
    assert b"Content" in response.data


def test_announce_add_check(test_client):
    """"""
    response = test_client.post(
        url_for(module_info["module_name"] + ".add_check"),
        data=dict(title="abc", content="def"),
        follow_redirects=True,
    )
    assert response.status_code == 200

    # check if message was added successfully
    response = test_client.get(url_for(module_info["module_name"] + ".list"))
    assert response.status_code == 200
    assert b"abc" in response.data
    assert b"def" in response.data


def test_announce_add_check_wrong(test_client):
    """"""
    response = test_client.post(
        url_for(module_info["module_name"] + ".add_check"),
        data=dict(title="", content="abc_wrong"),
        follow_redirects=True,
    )

    announcement = Announcement.query.filter(
        Announcement.content == "abc_wrong"
    ).first()
    assert announcement is None


def test_announce_edit_check(test_client):
    """"""
    announcement = Announcement(title="abcx", content="def")
    announcement.save()

    assert Announcement.query.get(1).title == "abcx"

    response = test_client.post(
        url_for(module_info["module_name"] + ".edit_check", announce_id=1),
        data=dict(title="abcxd", content="def"),
        follow_redirects=True,
    )
    assert response.status_code == 200

    # check if message was added successfully
    response = test_client.get(url_for(module_info["module_name"] + ".list"))
    assert response.status_code == 200
    assert b"abcxd" in response.data
    assert b"def" in response.data
