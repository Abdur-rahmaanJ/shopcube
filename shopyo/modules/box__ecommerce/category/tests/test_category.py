"""
This file (test_category.py) contains the functional tests
for the `category` blueprint.

These tests use GETs and POSTs to different URLs to check
for the proper behavior of the `category` blueprint.
"""
import os
import json
import pytest
from flask import url_for, request
from modules.box__ecommerce.category.models import Category
from modules.box__ecommerce.category.models import SubCategory

dirpath = os.path.dirname(os.path.abspath(__file__))
module_path = os.path.dirname(dirpath)

module_info = None

with open(os.path.join(module_path, "info.json")) as f:
    module_info = json.load(f)


class TestCategoryInvalidAuth:
    """
    Test all category routes for correct user authentication
    """

    routes_get = [
        module_info["dashboard"],
        "/add",
        "/<name>/delete",
        "/<category_name>/img/<filename>/delete",
        "/update",
        f"{module_info['dashboard']}/edit/<category_name>",
        "/check/<category_name>",
        "/file/<filename>",
        f"{module_info['dashboard']}/<category_name>/sub/",
        f"{module_info['dashboard']}/<category_name>/sub/add",
        f"{module_info['dashboard']}/sub/<subcategory_id>/img/edit",
        "/sub/<subcategory_id>/name/edit",
        "/sub/<subcategory_id>/img/edit",
        "/sub/<subcategory_id>/img/<filename>/delete",
        "/sub/<subcategory_id>/delete",
        "/sub/file/<filename>",
        f"/<category_id>{module_info['dashboard']}/sub",
    ]

    routes_post = [
        "/add",
        "/update",
        f"{module_info['dashboard']}/<category_name>/sub/add",
        "/sub/<subcategory_id>/name/edit",
        "/sub/<subcategory_id>/img/edit",
    ]

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
class TestCategoryApi:
    def test_category_dashboard_page_get(self, test_client):
        response = test_client.get(url_for("category.dashboard"))

        assert response.status_code == 200
        assert b"Category" in response.data

    def test_category_add_page_get(self, test_client):
        response = test_client.get(url_for("category.add"))

        assert response.status_code == 200
        assert b"name" in response.data
        assert b"image" in response.data

    def test_category_add_empty_name_post(self, test_client):
        response = test_client.post(
            url_for("category.add"),
            data=dict(name="   "),
            follow_redirects=True,
        )

        assert response.status_code == 200
        assert b"Category name cannot be empty" in response.data
        assert request.path == url_for("category.add")

    def test_category_add_uncategorized_as_name_post(self, test_client):
        response = test_client.post(
            url_for("category.add"),
            data=dict(name="uncategorized"),
            follow_redirects=True,
        )

        assert response.status_code == 200
        assert b"Category cannot be named as uncategorised" in response.data

    def test_category_add_uncategorised_as_name_post(self, test_client):
        response = test_client.post(
            url_for("category.add"),
            data=dict(name=" uncategorised"),
            follow_redirects=True,
        )

        assert response.status_code == 200
        assert b"Category cannot be named as uncategorised" in response.data

    def test_category_add_existing_category_name_post(self, test_client):
        Category.create(name="category")
        response = test_client.post(
            url_for("category.add"),
            data=dict(name="category"),
            follow_redirects=True,
        )

        assert response.status_code == 200
        assert b'Category "category" already exists' in response.data
        assert Category.query.count() == 1

    def test_category_add_unique_category_name_post(self, test_client):
        response = test_client.post(
            url_for("category.add"),
            data=dict(name="category"),
            follow_redirects=True,
        )
        added_category = Category.query.filter(
            Category.name == "category"
        ).all()

        assert response.status_code == 200
        assert b'Category "category" added successfully' in response.data
        assert len(added_category) == 1

    def test_category_add_name_with_lower_and_upper_post(self, test_client):
        response = test_client.post(
            url_for("category.add"),
            data=dict(name="CatEgorY"),
            follow_redirects=True,
        )
        added_category = Category.query.filter(
            Category.name == "category"
        ).all()

        assert response.status_code == 200
        assert b'Category "category" added successfully' in response.data
        assert len(added_category) == 1

    def test_category_add_name_with_leading_trailing_space(self, test_client):
        response = test_client.post(
            url_for("category.add"),
            data=dict(name="   category   "),
            follow_redirects=True,
        )
        added_category = Category.query.filter(
            Category.name == "category"
        ).all()

        assert response.status_code == 200
        assert b'Category "category" added successfully' in response.data
        assert len(added_category) == 1

    def test_category_delete_existing_category_get(self, test_client):
        Category.create(name="category")
        response = test_client.get(
            url_for("category.delete", name="category"),
            follow_redirects=True,
        )
        query = Category.query.filter(Category.name == "category").scalar()

        assert b'Category "category" successfully deleted' in response.data
        assert request.path == url_for("category.dashboard")
        assert query is None

    def test_category_delete_nonexisting_category_get(self, test_client):
        response = test_client.get(
            url_for("category.delete", name="category"),
            follow_redirects=True,
        )

        assert response.status_code == 200
        assert request.path == url_for("category.dashboard")
        assert b'Category "category" does not exist.' in response.data

    def test_category_delete_cat_with_subcategory_get(self, test_client):
        # add a category with subcategoires
        category = Category(name="category")
        subcategory = SubCategory(name="subcategory")
        category.subcategories.append(subcategory)
        category.save()

        response = test_client.get(
            url_for("category.delete", name="category"),
            follow_redirects=True,
        )

        assert response.status_code == 200
        assert request.path == url_for("category.dashboard")
        assert (
            b'Please delete all subcategories for category "category"'
            in response.data
        )

    def test_category_delete_cat_named_uncategorised_get(self, test_client):
        response = test_client.get(
            url_for("category.delete", name="uncategorised"),
            follow_redirects=True,
        )

        assert response.status_code == 200
        assert request.path == url_for("category.dashboard")
        assert b"Cannot delete category uncategorised" in response.data

    def test_category_delete_cat_name_which_is_empty_get(self, test_client):
        response = test_client.get(
            url_for("category.delete", name=" "), follow_redirects=True
        )

        assert response.status_code == 200
        assert request.path == url_for("category.dashboard")
        assert b"Cannot delete a category with no name" in response.data

    def test_category_add_nonexisting_subcategory_post(self, test_client):
        Category.create(name="category")
        response = test_client.post(
            url_for("category.add_sub", category_name="category"),
            data=dict(name="subcategory"),
            follow_redirects=True,
        )
        subcat = SubCategory.query.filter(
            SubCategory.name == "subcategory"
        ).scalar()

        assert response.status_code == 200
        assert request.path == url_for(
            "category.manage_sub", category_name="category"
        )
        assert subcat is not None
        assert subcat.category is not None
        assert subcat.category.name == "category"

    def test_category_add_existing_subcategory_post(self, test_client):
        category = Category(name="category1")
        subcategory = SubCategory(name="subcategory1")
        category.subcategories.append(subcategory)
        category.save()

        response = test_client.post(
            url_for("category.add_sub", category_name="category1"),
            data=dict(name="subcategory1"),
            follow_redirects=True,
        )
        subcategories = SubCategory.query.count()

        assert response.status_code == 200
        assert b"Name already exists for category" in response.data
        assert subcategories == 1

    def test_category_add_subcat_name_which_is_empty_get(self, test_client):
        Category.create(name="category1")
        response = test_client.post(
            url_for("category.add_sub", category_name="category1"),
            data=dict(name="  "),
            follow_redirects=True,
        )
        subcategories = SubCategory.query.count()

        assert response.status_code == 200
        assert b"Name cannot be empty" in response.data
        assert subcategories == 0

    def test_category_add_existing_subcat_with_spaces_post(self, test_client):
        category = Category(name="category1")
        subcategory = SubCategory(name="subcategory1")
        category.subcategories.append(subcategory)
        category.save()

        response = test_client.post(
            url_for("category.add_sub", category_name="category1"),
            data=dict(name="   subcategory1   "),
            follow_redirects=True,
        )
        subcategories = SubCategory.query.count()

        assert response.status_code == 200
        assert b"Name already exists for category" in response.data
        assert subcategories == 1

    def test_category_add_subcat_to_nonexisting_cat_post(self, test_client):
        response = test_client.post(
            url_for("category.add_sub", category_name="category"),
            data=dict(name="subcategory"),
            follow_redirects=True,
        )
        subcategories = SubCategory.query.count()

        assert response.status_code == 400
        assert b"category does not exist" in response.data
        assert subcategories == 0
