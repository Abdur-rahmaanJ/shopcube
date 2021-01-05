"""
This file (test_category.py) contains the functional tests
for the `category` blueprint.

These tests use GETs and POSTs to different URLs to check
for the proper behavior of the `category` blueprint.
"""

from flask import url_for, request
from modules.box__ecommerce.category.models import Category, SubCategory


def test_category_dashboard_page(test_client):
    """
    GIVEN a Flask application configured for testing,
    WHEN the category's dashboard page is requested (GET)
    THEN check that the response is valid
    """
    # Logout and try to access the category dashboard. It should redirect
    response = test_client.get(url_for("login.logout"), follow_redirects=True)
    assert response.status_code == 200
    assert request.path == url_for("login.login")

    # check request to category correctly redirects to login page
    response = test_client.get(
        url_for("category.dashboard"), follow_redirects=True
    )
    assert response.status_code == 200
    assert request.path == url_for("login.login")

    # Login and try to access the category dashboard. It should return OK
    response = test_client.post(
        url_for("login.login"),
        data=dict(email="admin1@domain.com", password="pass"),
        follow_redirects=True,
    )

    # check if successfully logged in
    assert response.status_code == 200

    # After successfull login, category dashboard can be accessed
    response = test_client.get(url_for("category.dashboard"))
    assert response.status_code == 200
    assert b"Category" in response.data


def test_category_add_get(test_client):
    """
    GIVEN a Flask application configured for testing,
    WHEN the category's dashboard page is requested (GET)
    THEN check that the response is valid
    """
    # Logout and try to access the category dashboard. It should redirect
    response = test_client.get(url_for("login.logout"), follow_redirects=True)
    assert response.status_code == 200
    assert request.path == url_for("login.login")

    # check request to contact correctly redirects to login page
    response = test_client.get(url_for("category.add"), follow_redirects=True)
    response.status_code == 200
    assert request.path == url_for("login.login")
    # Login and try to access the category dashboard. It should return OK
    response = test_client.post(
        url_for("login.login"),
        data=dict(email="admin1@domain.com", password="pass"),
        follow_redirects=True,
    )

    # check if successfully logged in
    assert response.status_code == 200

    # check add route GET response is valid
    response = test_client.get(url_for("category.add"))
    assert response.status_code == 200
    assert b"name" in response.data
    assert b"image" in response.data


def test_category_add_post_invalid(test_client, db_session):
    """
    GIVEN a Flask application configured for testing, and a db session
    WHEN the invalid POST requests are made to category add page
    THEN check that the responses are valid
    """
    # should not allow adding empty string category
    response = test_client.post(
        url_for("category.add"), data=dict(name="   "), follow_redirects=True,
    )
    assert response.status_code == 200
    assert b"Category name cannot be empty" in response.data

    # should not allow adding category name "uncategorized"
    # which is case-insensitive
    response = test_client.post(
        url_for("category.add"),
        data=dict(name=" uncateGoriZed  "),
        follow_redirects=True,
    )
    assert response.status_code == 200
    assert b"Category cannot be named as uncategorised" in response.data

    # should not allow adding alternateive spelling of uncategorise
    response = test_client.post(
        url_for("category.add"),
        data=dict(name=" uncategoriseD"),
        follow_redirects=True,
    )
    assert response.status_code == 200
    assert b"Category cannot be named as uncategorised" in response.data

    # add a category and then try adding the same one again
    category = Category(name="test-exiting-category")
    db_session.add(category)
    db_session.commit()
    assert db_session.query(Category).count() == 1

    # should not allow adding category whose name already exists
    response = test_client.post(
        url_for("category.add"),
        data=dict(name="test-exiting-category"),
        follow_redirects=True,
    )
    assert response.status_code == 200

    assert b'Category "test-exiting-category" already exists' in response.data
    assert db_session.query(Category).count() == 1


def test_category_add_post_valid(test_client, db_session):
    """
    GIVEN a Flask application configured for testing, and a db session
    WHEN the a valid POST request is made to category add page
    THEN check that the response is valid
    """
    # make sure no category is in database at the start
    assert db_session.query(Category).count() == 0

    # add a valid category
    response = test_client.post(
        url_for("category.add"),
        data=dict(name="test-valid-category-1"),
        follow_redirects=True,
    )

    # it should succesfully be added
    assert response.status_code == 200

    assert (
        b'Category "test-valid-category-1" added successfully' in response.data
    )
    assert db_session.query(Category).count() == 1

    # make sure the correct category exits
    row = (
        db_session.query(Category)
        .filter(Category.name == "test-valid-category-1")
        .scalar()
    )
    assert row.name == "test-valid-category-1"


def test_category_delete_get_valid(test_client, db_session):
    """
    GIVEN a Flask application configured for testing, and db session
    WHEN the valid GET requests are made to category add page
    THEN check that the responses are valid
    """
    # add a category that is to be deleted
    category = Category(name="test-delete-category")
    db_session.add(category)
    db_session.commit()
    assert db_session.query(Category).count() == 1

    # make sure the correct category exits
    row = (
        db_session.query(Category)
        .filter(Category.name == "test-delete-category")
        .scalar()
    )
    assert row and row.name == "test-delete-category"

    # Logout and try to access category delete route. It should redirect
    response = test_client.get(url_for("login.logout"), follow_redirects=True)
    assert response.status_code == 200
    assert request.path == url_for("login.login")
    # Check request to category delete correctly redirects to login page
    response = test_client.get(
        url_for("category.delete", name="test-delete-category"),
        follow_redirects=True,
    )
    response.status_code == 200
    assert request.path == url_for("login.login")

    # Login and try to access the category delete route. It should return OK
    response = test_client.post(
        url_for("login.login"),
        data=dict(email="admin1@domain.com", password="pass"),
        follow_redirects=True,
    )
    # Check if successfully logged in
    assert response.status_code == 200
    # after login we should be able to successfully delete category
    response = test_client.get(
        url_for("category.delete", name="test-delete-category"),
        follow_redirects=True,
    )
    assert (
        b'Category "test-delete-category" sucessfully deleted' in response.data
    )
    assert request.path == url_for("category.dashboard")
    row = (
        db_session.query(Category)
        .filter(Category.name == "test-delete-category")
        .scalar()
    )

    assert not row


def test_category_delete_invalid(test_client, db_session):
    """
    GIVEN a Flask application configured for testing, and a db session
    WHEN the invalid GET requests are made to category add page
    THEN check that the responses are valid
    """
    # make sure no category is in database at the start
    assert db_session.query(Category).count() == 0

    # Should not allow deleteing category named "uncategorised"
    response = test_client.get(
        url_for("category.delete", name="uncategorised"), follow_redirects=True
    )
    assert response.status_code == 200
    assert request.path == url_for("category.dashboard")
    assert b"Cannot delete category uncategorised" in response.data

    # Should not allow deleting category with empty name
    response = test_client.get(
        url_for("category.delete", name=" "), follow_redirects=True
    )
    assert response.status_code == 200
    assert request.path == url_for("category.dashboard")
    assert b"Cannot delete a category with no name" in response.data

    # Should not allow deleting category that does not exist
    response = test_client.get(
        url_for("category.delete", name="test-delete-category"),
        follow_redirects=True,
    )
    assert response.status_code == 200
    assert request.path == url_for("category.dashboard")
    assert b'Category "test-delete-category" does not exist.' in response.data

    # add a category with subcategoires
    category = Category(name="test-delete-category")
    subcategory1 = SubCategory(name="test-subcat-1")
    category.subcategories.append(subcategory1)
    db_session.add(category)
    db_session.add(subcategory1)
    db_session.commit()

    # should not allow deleting a category with subcategories
    response = test_client.get(
        url_for("category.delete", name="test-delete-category"),
        follow_redirects=True,
    )
    assert response.status_code == 200
    assert request.path == url_for("category.dashboard")
    assert (
        b"Please delete all subcategories for category "
        + b'"test-delete-category"'
        in response.data
    )

    # Add another subcategory to the same category
    subcategory2 = SubCategory(name="test-subcat-2")
    category.subcategories.append(subcategory2)
    db_session.add(subcategory2)
    db_session.commit()

    # Still should not allow deleting a category with subcategories
    response = test_client.get(
        url_for("category.delete", name="test-delete-category"),
        follow_redirects=True,
    )
    assert response.status_code == 200
    assert request.path == url_for("category.dashboard")
    assert (
        b"Please delete all subcategories for category "
        + b'"test-delete-category"'
        in response.data
    )

    # remove all subcategories
    db_session.delete(subcategory1)
    db_session.delete(subcategory2)
    db_session.commit()

    # should now allow deleting a category with no subcategory
    response = test_client.get(
        url_for("category.delete", name="test-delete-category"),
        follow_redirects=True,
    )
    assert response.status_code == 200
    assert request.path == url_for("category.dashboard")
    assert (
        b'Category "test-delete-category" sucessfully deleted' in response.data
    )
    assert db_session.query(Category).count() == 0
    assert db_session.query(SubCategory).count() == 0


def test_category_sub_add_valid(test_client, auth, non_admin_user, db_session):
    """
    GIVEN a Flask application configured for testing,
    auth class for user login and logout, a non admin user,
    and a database session,
    WHEN the adding sub category with valid parameters
    THEN check that the response is valid
    """
    # make sure no Categories as of yet
    assert db_session.query(Category).count() == 0

    # add a test category
    category = Category(name="test-category")
    db_session.add(category)
    db_session.commit()
    assert db_session.query(Category).count() == 1

    # logout
    auth.logout()

    # access to category add_sub should not be
    # allowed since not logged in
    response = test_client.post(
        url_for("category.add_sub", category_name="test-category"),
        data=dict(name="test-sub-category"),
        follow_redirects=True,
    )
    assert response.status_code == 200
    assert request.path == url_for("login.login")
    assert db_session.query(SubCategory).count() == 0

    # login to the app with a non admin user
    auth.login(non_admin_user)

    # should successfully create the subcategory
    response = test_client.post(
        url_for("category.add_sub", category_name="test-category"),
        data=dict(name="test-sub-category"),
        follow_redirects=True,
    )
    assert request.path == url_for(
        "category.manage_sub",
        category_name="test-category"
    )
    exiting_subcat = (
        db_session.query(SubCategory)
        .filter(SubCategory.name == "test-sub-category")
        .scalar()
    )
    assert exiting_subcat and exiting_subcat.category.name == "test-category"
    assert db_session.query(SubCategory).count() == 1


def test_category_sub_add_invalid(test_client, auth,
                                  non_admin_user, db_session):
    """
    GIVEN a Flask application configured for testing,
    auth class for user login and logout, a non admin user,
    and a database session,
    WHEN the adding sub category with invalid parameters
    THEN check that the response is valid
    """
    # make sure no Categories as of yet
    assert db_session.query(Category).count() == 0
    assert db_session.query(SubCategory).count() == 0

    # login to the app with a non admin user
    auth.login(non_admin_user)

    # add a test category and a subcategory
    category = Category(name="test-category")
    subcategory = SubCategory(name="test-sub-category")
    category.subcategories.append(subcategory)
    db_session.add(category)
    db_session.add(subcategory)
    db_session.commit()
    assert db_session.query(Category).count() == 1
    assert db_session.query(SubCategory).count() == 1

    # should not allow adding existing subcategory
    response = test_client.post(
        url_for("category.add_sub", category_name="test-category"),
        data=dict(name="test-sub-category"),
        follow_redirects=True,
    )
    assert b"Name already exists for category" in response.data
    assert db_session.query(SubCategory).count() == 1

    # should not allow adding empty category
    response = test_client.post(
        url_for("category.add_sub", category_name="test-category"),
        data=dict(name="  "),
        follow_redirects=True,
    )
    assert b"Name cannot be empty" in response.data
    assert db_session.query(SubCategory).count() == 1

    # should not allow adding existing category with leading
    # trailing spaces
    response = test_client.post(
        url_for("category.add_sub", category_name="test-category"),
        data=dict(name="   test-sub-category   "),
        follow_redirects=True,
    )
    assert b"Name already exists for category" in response.data
    assert db_session.query(SubCategory).count() == 1
