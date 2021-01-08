"""
This file (test_admin.py) contains the functional tests for
the `admin` blueprint.

These tests use GETs and POSTs to different endpoints to check
for the proper behavior of the `admin` blueprint.
"""
from flask import request
from flask import url_for
from modules.box__default.admin.models import Role, User


def test_admin_home_page(test_client, auth, admin_user, non_admin_user):
    """
    GIVEN a Flask application configured for testing, an admin user,
    and a non admin user
    WHEN the '/admin' page is requested (GET) by user with admin privileges
    THEN check that the response is valid
    """
    # logout
    auth.logout()

    # Accessing admin paged without login should redirect
    response = test_client.get(
        url_for("admin.user_list"), follow_redirects=True
    )
    assert response.status_code == 200
    assert request.path == url_for("login.login")

    # Login with admin credentials
    auth.login(admin_user)

    # Allow user with admin privilege to a access the admin page
    response = test_client.get(url_for("admin.user_list"))
    assert response.status_code == 200
    assert b"Admin" in response.data
    assert b"id" in response.data
    assert b"Email" in response.data
    assert b"Password" in response.data
    assert b"Roles" in response.data

    # Login with non-admin credentials
    auth.login(non_admin_user)

    # Redirect user with non-admin privilege to dashboard
    response = test_client.get(
        url_for("admin.user_list"), follow_redirects=True
    )
    assert response.status_code == 200
    assert request.path == url_for("dashboard.index")
    assert b"You need to be an admin to view this page" in response.data


def test_admin_add_get(test_client, admin_user, non_admin_user, auth):
    """
    GIVEN a Flask application configured for testing, an admin user,
    a non admin user, and auth class for user login and logout
    WHEN the '/admin/add', '/admin/roles' page are requested (GET) by user with
    admin privileges
    THEN check that the response is valid
    """
    # Access to admin add route should not be allowed if not logged in
    auth.logout()
    response = test_client.get(
        url_for("admin.user_add"), follow_redirects=True
    )
    assert response.status_code == 200
    assert request.path == url_for("login.login")

    # Login with non admin should not allow accessing the admin add
    auth.login(non_admin_user)
    response = test_client.get(
        url_for("admin.user_add"), follow_redirects=True
    )
    assert response.status_code == 200
    assert request.path == url_for("dashboard.index")

    # Login with admin credentials
    auth.login(admin_user)

    # check if add route is working
    response = test_client.get(url_for("admin.user_add"))
    assert response.status_code == 200
    assert b"Email" in response.data
    assert b"Password" in response.data
    assert b"First Name" in response.data
    assert b"Last Name" in response.data
    assert b"Admin User" in response.data


def test_admin_add_post(test_client, admin_user, auth, db_session):
    """
    GIVEN a Flask application configured for testing, a non admin user
    auth class for user login and logout, and a database session,
    WHEN making POST request to add users to admin route
    THEN check that the response is valid for different cases
    """
    # login with admin user
    auth.login(admin_user)

    # create a role
    assert db_session.query(Role).count() == 0
    role1 = Role(name="test1-role")
    role2 = Role(name="test2-role")
    db_session.add(role1)
    db_session.add(role2)
    db_session.commit()
    assert db_session.query(Role).count() == 2

    # intialize the data that will be posted
    data = {
        "email": "test@gmail.com",
        "password": "pass",
        "first_name": "Test",
        "last_name": "User",
        "is_admin": "",
        "role_" + str(role1.id): "",
        "role_" + str(role2.id): ""
    }

    # Do POST request to add the test user
    # with the two roles initialized above
    response = test_client.post(
        url_for("admin.user_add"),
        data=data,
        follow_redirects=True
    )

    # check if the user and roles are correctly added
    test_user = (
        db_session.query(User)
        .filter(User.email == "test@gmail.com")
        .scalar()
    )
    assert test_user and test_user.first_name == "Test"
    assert test_user.last_name == "User"
    assert not test_user.is_admin
    assert test_user.roles and len(test_user.roles) == 2
    assert role1.users[0].email == "test@gmail.com"
    assert role2.users[0].email == "test@gmail.com"

    # Should not allow adding the same user again
    response = test_client.post(
        url_for("admin.user_add"),
        data=data,
        follow_redirects=True
    )
    test_users = (
        db_session.query(User)
        .filter(User.email == "test@gmail.com")
        .count()
    )
    assert response.status_code == 200
    assert b"User with same email already exists"
    assert test_users == 1


def test_admin_roles_get(test_client, admin_user, non_admin_user, auth):
    """
    GIVEN a Flask application configured for testing, an admin user
    a non admin user, and an auth class for user login and logout,
    WHEN making GET request to roles route
    THEN check that the response is valid
    """
    # Access to admin roles route should not be allowed if not logged in
    auth.logout()
    response = test_client.get(url_for("admin.roles"), follow_redirects=True)
    assert response.status_code == 200
    assert request.path == url_for("login.login")

    # Login with non admin user
    auth.login(non_admin_user)
    response = test_client.get(url_for("admin.roles"), follow_redirects=True)
    assert response.status_code == 200
    assert request.path == url_for("dashboard.index")

    # Login with admin credentials
    auth.login(admin_user)

    # check if the roles route is working
    response = test_client.get(url_for("admin.roles"))
    assert response.status_code == 200
    assert b"Roles" in response.data
