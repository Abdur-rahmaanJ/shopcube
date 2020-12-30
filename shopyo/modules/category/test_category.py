"""
This file (test_category.py) contains the functional tests
for the `category` blueprint.

These tests use GETs and POSTs to different URLs to check
for the proper behavior of the `category` blueprint.
"""
from flask import url_for, request
from modules.category.models import Category


def test_category_dashboard_page(test_client):
    """
    GIVEN a Flask application configured for testing,
    WHEN the category's dashboard page is requested (GET)
    THEN check that the response is valid
    """
    # Logout and try to access the category dashboard. It should redirect
    response = test_client.get(url_for('login.logout'), follow_redirects=True)
    assert response.status_code == 200
    assert b"Successfully logged out" in response.data

    # check request to contact correctly redirects to login page
    response = test_client.get(
        url_for('category.dashboard'), follow_redirects=True)
    assert request.path == url_for('login.login')

    # Login and try to access the category dashboard. It should return OK
    response = test_client.post(
        url_for('login.login'),
        data=dict(email="admin1@domain.com", password="pass"),
        follow_redirects=True,
    )

    # check if successfully logged in
    assert response.status_code == 200

    response = test_client.get(url_for('category.dashboard'))
    assert response.status_code == 200
    assert b"Category" in response.data


def test_category_add_get(test_client, init_database):
    """
    GIVEN a Flask application configured for testing,
    WHEN the category's dashboard page is requested (GET)
    THEN check that the response is valid
    """
    # Logout and try to access the category dashboard. It should redirect
    response = test_client.get(url_for('login.logout'), follow_redirects=True)
    assert response.status_code == 200
    assert b"Successfully logged out" in response.data

    # check request to contact correctly redirects to login page
    response = test_client.get(url_for('category.add'), follow_redirects=True)
    assert request.path == url_for('login.login')

    # Login and try to access the category dashboard. It should return OK
    response = test_client.post(
        url_for('login.login'),
        data=dict(email="admin1@domain.com", password="pass"),
        follow_redirects=True,
    )

    # check if successfully logged in
    assert response.status_code == 200

    # check add route GET response is valid
    response = test_client.get(url_for('category.add'))
    assert response.status_code == 200
    assert b"name" in response.data
    assert b"image" in response.data


def test_category_add_post_invalid(test_client, init_database):
    """
    GIVEN a Flask application configured for testing, and an initial database
    WHEN the invalid POST requests are made to category add page
    THEN check that the responses are valid
    """
    # should not allow adding empty string category
    response = test_client.post(
        url_for('category.add'),
        data=dict(name="   "),
        follow_redirects=True,
    )
    assert response.status_code == 200
    assert b"Category name cannot be empty" in response.data

    # should not allow adding category name "uncategorized"
    # which is case-insensitive
    response = test_client.post(
        url_for('category.add'),
        data=dict(name=" uncateGoriZed  "),
        follow_redirects=True,
    )
    assert response.status_code == 200
    assert b"Category cannot be named as uncategorised" in response.data

    # should not allow adding alternateive spelling of uncategorise
    response = test_client.post(
        url_for('category.add'),
        data=dict(name=" uncategoriseD"),
        follow_redirects=True,
    )
    assert response.status_code == 200
    assert b"Category cannot be named as uncategorised" in response.data

    # add a category and then try adding the same one again
    category = Category(name="test-exiting-category")
    init_database.session.add(category)
    assert init_database.session.query(Category).count() == 1

    # should not allow adding category whose name already exists
    response = test_client.post(
        url_for('category.add'),
        data=dict(name="test-exiting-category"),
        follow_redirects=True,
    )
    assert response.status_code == 200
    assert b"Category already exists" in response.data
    assert init_database.session.query(Category).count() == 1

    # remove the added category so it does not affect future tests.
    # Ideally want to use pytest-flask-sqlalchemy plugin for auto tear
    # down but currently giving a warning. Also if any of the above
    # asserts fail then we never reach this code and future tests might
    # fail as well. NEED TO FIX THIS
    init_database.session.rollback()
    assert init_database.session.query(Category).count() == 0


def test_category_add_post_valid(test_client, init_database):
    """
    GIVEN a Flask application configured for testing, and an initial database
    WHEN the a valid POST request is made to category add page
    THEN check that the response is valid
    """
    # make sure no category is in database at the start
    assert init_database.session.query(Category).count() == 0

    # add a valid category
    response = test_client.post(
        url_for('category.add'),
        data=dict(name="test-valid-category-1"),
        follow_redirects=True,
    )

    # it should succesfully be added
    assert response.status_code == 200
    assert b"Category added successfully" in response.data
    assert init_database.session.query(Category).count() == 1

    # make sure the correct category exits
    row = (init_database.session.query(Category).
           filter(Category.name == 'test-valid-category-1').scalar())
    assert row.name == 'test-valid-category-1'

    # remove the added category so it does not affect future tests.
    # Ideally want to use pytest-flask-sqlalchemy plugin for auto tear
    # down but currently giving a warning. Also if any of the above
    # asserts fail then we never reach this code and future tests might
    # fail as well. NEED TO FIX THIS
    row.delete()
    assert init_database.session.query(Category).count() == 0
