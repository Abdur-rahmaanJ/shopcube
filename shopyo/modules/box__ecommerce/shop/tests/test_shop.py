"""
This file (test_shopy.py) contains the functional tests for
the `shopy` blueprint.

These tests use GETs and POSTs to different endpoints to check
for the proper behavior of the `shop` blueprint.
"""
import pytest


@pytest.mark.order("first")
def test_shop_home_page(test_client):
    """
    GIVEN a Flask application configured for testing,
    WHEN the '/' page is requested (GET)
    THEN check that the response is valid
    """
    # '/' redirects to /shop/home
    response = test_client.get("/", follow_redirects=True)
    assert response.status_code == 200
