"""
This file (test_admin.py) contains the functional tests for
the `admin` blueprint.

These tests use GETs and POSTs to different endpoints to check
for the proper behavior of the `admin` blueprint.
"""
import os
import json
import pytest
from flask import request
from flask import url_for
from modules.box__default.auth.models import Role
from modules.box__default.auth.models import User
from modules.box__default.auth.models import role_user_bridge


dirpath = os.path.dirname(os.path.abspath(__file__))
module_path = os.path.dirname(dirpath)

module_info = None

with open(os.path.join(module_path, "info.json")) as f:
    module_info = json.load(f)


class TestAdminInvalidAccess:
    """
    Test all admin routes for correct user authentication
    """

    routes_get = [
        "/",
        "/add",
        "/delete/<id>",
        "/edit/<id>",
        "/roles",
        "/roles/<role_id>/delete",
    ]

    routes_post = ["/update", "/roles/update", "/roles/add", "/add"]

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

    @pytest.mark.usefixtures("login_non_admin_user")
    @pytest.mark.parametrize("route", routes_get)
    def test_no_admin_access_if_not_admin_get(self, test_client, route):
        response = test_client.get(
            f"{module_info['url_prefix']}{route}", follow_redirects=True
        )

        assert response.status_code == 200
        assert request.path == url_for("dashboard.index")
        assert b"You need to be an admin to view this page" in response.data

    @pytest.mark.usefixtures("login_non_admin_user")
    @pytest.mark.parametrize("route", routes_post)
    def test_no_admin_access_if_not_admin_post(self, test_client, route):
        response = test_client.post(
            f"{module_info['url_prefix']}{route}", follow_redirects=True
        )

        assert response.status_code == 200
        assert request.path == url_for("dashboard.index")
        assert b"You need to be an admin to view this page" in response.data


@pytest.mark.usefixtures("login_admin_user")
class TestAdminEndpoints:
    """
    Test all admin api post and get requests
    """

    def test_admin_user_list_get(self, test_client):
        response = test_client.get(f"{module_info['url_prefix']}/")

        assert response.status_code == 200
        assert b"Admin" in response.data
        assert b"id" in response.data
        assert b"Email" in response.data
        assert b"Password" in response.data
        assert b"Roles" in response.data

    def test_admin_add_get(self, test_client):
        response = test_client.get(f"{module_info['url_prefix']}/add")

        assert response.status_code == 200
        assert b"Email" in response.data
        assert b"Password" in response.data
        assert b"First Name" in response.data
        assert b"Last Name" in response.data
        assert b"Admin User" in response.data

    def test_admin_add_unique_user_post(self, test_client):
        role1 = Role.create(name="test1-role")
        role2 = Role.create(name="test2-role")
        data = {
            "email": "test@gmail.com",
            "password": "pass",
            "first_name": "Test",
            "last_name": "User",
            "is_admin": "",
            f"role_{role1.id}": "",
            f"role_{role2.id}": "",
        }

        test_client.post(
            f"{module_info['url_prefix']}/add",
            data=data,
            follow_redirects=True,
        )
        test_user = User.query.filter(User.email == "test@gmail.com").scalar()

        assert test_user is not None
        assert test_user.first_name == "Test"
        assert test_user.last_name == "User"
        assert test_user.is_admin is False
        assert test_user.roles is not None
        assert len(test_user.roles) == 2
        assert role1.users[0].email == "test@gmail.com"
        assert role2.users[0].email == "test@gmail.com"

    def test_admin_add_existing_user_post(self, test_client):
        User.create(email="test@gmail.com", password="pass")
        data = {
            "email": "test@gmail.com",
            "password": "pass",
            "first_name": "Test",
            "last_name": "User",
            "is_admin": "",
        }

        response = test_client.post(
            f"{module_info['url_prefix']}/add",
            data=data,
            follow_redirects=True,
        )
        test_users = User.query.filter(User.email == "test@gmail.com").count()

        assert response.status_code == 200
        assert b"User with same email already exists" in response.data
        assert test_users == 1

    def test_admin_delete_existing_user_get(self, test_client):
        user = User(email="test@gmail.com", password="pass")
        role1 = Role(name="test1-role")
        role2 = Role(name="test2-role")
        user.roles = [role1, role2]
        user.save()

        response = test_client.get(
            f"{module_info['url_prefix']}/delete/{user.id}",
            follow_redirects=True,
        )
        test_user = User.query.filter(User.email == user.email).scalar()
        test_roles = Role.query.count()
        user_role = (
            User.query.join(role_user_bridge)
            .join(Role)
            .filter(User.id == user.id)
            .scalar()
        )

        assert response.status_code == 200
        assert test_user is None
        assert user_role is None
        assert test_roles == 2

    def test_admin_delete_nonexisting_user_get(self, test_client):
        response = test_client.get(
            f"{module_info['url_prefix']}/delete/some_id",
            follow_redirects=True,
        )

        assert response.status_code == 200
        assert b"Unable to delete. Invalid user id" in response.data

    def test_admin_edit_existing_user_get(self, test_client):
        user = User.create(email="test@gmail.com", password="pass")

        response = test_client.get(
            f"{module_info['url_prefix']}/edit/{user.id}",
        )

        assert response.status_code == 200
        assert b"test@gmail.com" in response.data
        assert b"Edit User" in response.data

    def test_admin_edit_nonexisting_user_get(self, test_client):
        response = test_client.get(
            f"{module_info['url_prefix']}/edit/some-id", follow_redirects=True
        )

        assert response.status_code == 200
        assert b"Invalid user id" in response.data
        assert request.path == f"{module_info['url_prefix']}/"

    def test_admin_update_user_adding_new_roles_to_user(self, test_client):
        user = User.create(email="foo@gmail.com", password="pass")
        role1 = Role.create(name="test1-role")
        role2 = Role.create(name="test2-role")
        data = {
            "id": str(user.id),
            "email": "bar@gmail.com",
            "password": "newpass",
            "first_name": "Test",
            "last_name": "User",
            "is_admin": "",
            f"role_{role1.id}": "",
            f"role_{role2.id}": "",
        }

        response = test_client.post(
            f"{module_info['url_prefix']}/update",
            data=data,
            follow_redirects=True,
        )

        assert response.status_code == 200
        assert user.email == "bar@gmail.com"
        assert user.check_password("newpass")
        assert user.first_name == "Test"
        assert user.last_name == "User"
        assert len(user.roles) == 2
        assert role1.users[0].email == "bar@gmail.com"
        assert role2.users[0].email == "bar@gmail.com"

    def test_admin_update_user_remove_old_roles_from_user(self, test_client):
        user = User(email="foo@gmail.com", password="pass", is_admin=True)
        user.is_admin = True
        role1 = Role(name="test1-role")
        role2 = Role(name="test2-role")
        user.roles = [role1, role2]
        user.save()
        data = {
            "id": str(user.id),
            "email": "bar@gmail.com",
            "first_name": "Test",
            "last_name": "User",
            "password": "   ",
            "is_admin": None,
        }

        response = test_client.post(
            f"{module_info['url_prefix']}/update",
            data=data,
            follow_redirects=True,
        )

        assert response.status_code == 200
        assert user.email == "bar@gmail.com"
        assert user.check_password("pass")
        assert len(user.roles) == 0
        assert len(role1.users) == 0
        assert len(role2.users) == 0

    def test_admin_roles_get(self, test_client):
        response = test_client.get(f"{module_info['url_prefix']}/roles")

        assert response.status_code == 200
        assert b"Roles" in response.data

    def test_admin_roles_add_nonexisting_role_post(self, test_client):
        response = test_client.post(
            f"{module_info['url_prefix']}/roles/add",
            data=dict(name="new-role"),
            follow_redirects=True,
        )

        role = Role.query.filter(Role.name == "new-role").scalar()
        role_count = Role.query.count()

        assert response.status_code == 200
        assert role is not None
        assert role_count == 1

    def test_admin_roles_add_existing_role_post(self, test_client):
        Role.create(name="new-role")

        response = test_client.post(
            f"{module_info['url_prefix']}/roles/add",
            data=dict(name="new-role"),
            follow_redirects=True,
        )
        role_count = Role.query.count()
        role = Role.query.filter(Role.name == "new-role").scalar()

        assert response.status_code == 200
        assert b"Role already exists" in response.data
        assert role is not None
        assert role_count == 1

    def test_admin_roles_delete_nonexisting_role_get(self, test_client):
        response = test_client.get(
            f"{module_info['url_prefix']}/roles/some-id/delete",
            follow_redirects=True,
        )

        assert response.status_code == 200
        assert request.path == f"{module_info['url_prefix']}/roles"
        assert b"Unable to delete. Invalid role id" in response.data

    def test_admin_roles_delete_existing_role_get(self, test_client):
        role1 = Role.create(name="new-role1")
        role2 = Role.create(name="new-role2")

        response = test_client.get(
            f"{module_info['url_prefix']}/roles/{role1.id}/delete",
            follow_redirects=True,
        )
        roles = Role.query.all()

        assert response.status_code == 200
        assert request.path == f"{module_info['url_prefix']}/roles"
        assert b"Role successfully deleted" in response.data
        assert roles is not None
        assert roles[0].name == role2.name
        assert len(roles) == 1

    def test_admin_roles_update_nonexisting_role_post(self, test_client):
        response = test_client.post(
            f"{module_info['url_prefix']}/roles/update",
            data=dict(role_id="some-id"),
            follow_redirects=True,
        )
        roles = Role.query.count()

        assert response.status_code == 200
        assert request.path == f"{module_info['url_prefix']}/roles"
        assert b"Unable to update. Role does not exist" in response.data
        assert roles == 0

    def test_admin_roles_update_existing_role_post(self, test_client):
        new_role = Role.create(name="new-role1")

        response = test_client.post(
            f"{module_info['url_prefix']}/roles/update",
            data=dict(role_id=new_role.id, role_name="update-role"),
            follow_redirects=True,
        )
        role = Role.query.scalar()

        assert response.status_code == 200
        assert request.path == f"{module_info['url_prefix']}/roles"
        assert b"Role successfully updated" in response.data
        assert role is not None
        assert role.name == "update-role"
