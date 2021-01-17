"""
This file (test_admin.py) contains the functional tests for
the `admin` blueprint.

These tests use GETs and POSTs to different endpoints to check
for the proper behavior of the `admin` blueprint.
"""
import os
import json
from flask import request
from flask import url_for
import pytest
from modules.box__default.admin.models import Role
from modules.box__default.admin.models import User
from modules.box__default.admin.models import role_user_link


dirpath = os.path.dirname(os.path.abspath(__file__))
module_path = os.path.dirname(dirpath)

module_info = None
module_prefix = "/"

with open(os.path.join(module_path, 'info.json')) as f:
    module_info = json.load(f)
    module_prefix = module_info['url_prefix']


class TestAdminInvalidAuth:
    """
    Test all routes for correct user authentication
    """
    routes_get = [
        "/", "/add", "/delete/<id>", "/edit/<id>",
        "/roles", "/roles/<role_id>/delete",
    ]

    routes_post = [
        "/update", "/roles/update", "/roles/add", "/add"
    ]

    @pytest.mark.parametrize('route', routes_get)
    def test_redirect_if_not_logged_in_get(self, test_client, route, auth):
        auth.logout()
        response = test_client.get(
            module_info['url_prefix'] + route, follow_redirects=True
        )

        assert response.status_code == 200
        assert request.path == url_for("login.login")

    @pytest.mark.parametrize('route', routes_post)
    def test_redirect_if_not_logged_in_post(self, test_client, route, auth):
        auth.logout()
        response = test_client.post(
            module_info['url_prefix'] + route, follow_redirects=True
        )

        assert response.status_code == 200
        assert request.path == url_for("login.login")

    @pytest.mark.usefixtures("login_non_admin_user")
    @pytest.mark.parametrize('route', routes_get)
    def test_redirect_if_not_admin_get(self, test_client, route):
        response = test_client.get(
            module_info['url_prefix'] + route, follow_redirects=True
        )

        assert response.status_code == 200
        assert request.path == url_for("dashboard.index")
        assert b"You need to be an admin to view this page" in response.data

    @pytest.mark.usefixtures("login_non_admin_user")
    @pytest.mark.parametrize('route', routes_post)
    def test_redirect_if_not_admin_post(self, test_client, route):
        response = test_client.post(
            module_info['url_prefix'] + route, follow_redirects=True
        )

        assert response.status_code == 200
        assert request.path == url_for("dashboard.index")
        assert b"You need to be an admin to view this page" in response.data


@pytest.mark.usefixtures("login_admin_user")
class TestAdminAPI:

    def test_admin_user_list_get(self, test_client):
        response = test_client.get(module_info['url_prefix'] + "/")

        assert response.status_code == 200
        assert b"Admin" in response.data
        assert b"id" in response.data
        assert b"Email" in response.data
        assert b"Password" in response.data
        assert b"Roles" in response.data

    def test_admin_add_get(self, test_client):
        response = test_client.get(module_info['url_prefix'] + "/add")

        assert response.status_code == 200
        assert b"Email" in response.data
        assert b"Password" in response.data
        assert b"First Name" in response.data
        assert b"Last Name" in response.data
        assert b"Admin User" in response.data

    def test_admin_add_post_unique_user(self, test_client, db_session):
        role1 = Role(name="test1-role")
        role2 = Role(name="test2-role")
        db_session.add(role1)
        db_session.add(role2)
        db_session.commit()
        data = {
            "email": "test@gmail.com",
            "password": "pass",
            "first_name": "Test",
            "last_name": "User",
            "is_admin": "",
            "role_" + str(role1.id): "",
            "role_" + str(role2.id): ""
        }

        test_client.post(
            module_info['url_prefix'] + "/add",
            data=data,
            follow_redirects=True
        )
        test_user = (
            db_session.query(User)
            .filter(User.email == "test@gmail.com")
            .scalar()
        )

        assert test_user
        assert test_user.first_name == "Test"
        assert test_user.last_name == "User"
        assert not test_user.is_admin
        assert test_user.roles
        assert len(test_user.roles) == 2
        assert role1.users[0].email == "test@gmail.com"
        assert role2.users[0].email == "test@gmail.com"

    def test_admin_add_post_existing_user(self, test_client, db_session):
        user = User(email="test@gmail.com", password="pass")
        db_session.add(user)
        db_session.commit()
        data = {
            "email": "test@gmail.com",
            "password": "pass",
            "first_name": "Test",
            "last_name": "User",
            "is_admin": "",
        }

        response = test_client.post(
            module_info['url_prefix'] + "/add",
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

    def test_admin_delete_existing_user_get(self, test_client, db_session):
        user = User(email="test@gmail.com", password="pass")
        role1 = Role(name="test1-role")
        role2 = Role(name="test2-role")
        user.roles = [role1, role2]

        db_session.add(user)
        db_session.commit()
        response = test_client.get(
            module_info['url_prefix'] + "/delete/" + user.id,
            follow_redirects=True
        )
        test_user = (
            db_session.query(User)
            .filter(User.email == user.email)
            .scalar()
        )
        test_roles = (
            db_session.query(Role)
            .count()
        )
        user_role = (
            db_session.query(role_user_link).join(User).join(Role)
            .filter(User.id == user.id).all()
        )

        assert response.status_code == 200
        assert not test_user
        assert not user_role
        assert test_roles == 2

    def test_admin_delete_nonexisting_user_get(self, test_client):
        response = test_client.get(
            module_info['url_prefix'] + "/delete/some_id",
            follow_redirects=True
        )

        assert response.status_code == 200
        assert b"Unable to delete. Invalid user id"

    def test_admin_roles_get(self, test_client):
        response = test_client.get(module_info['url_prefix'] + "/roles")

        assert response.status_code == 200
        assert b"Roles" in response.data
