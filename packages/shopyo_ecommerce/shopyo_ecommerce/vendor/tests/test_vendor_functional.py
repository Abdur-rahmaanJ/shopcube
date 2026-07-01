import pytest
from flask import url_for
from shopyo_ecommerce.vendor.models import Vendor


def login_admin(test_client):
    test_client.post(url_for("shopyo_auth.login"), data=dict(email="admin2@domain.com", password="pass"), follow_redirects=True)
    return test_client


class TestVendorCrud:
    def test_vendor_add(self, test_client, db_session):
        login_admin(test_client)
        response = test_client.post(url_for("shopyo_ecommerce.vendor.add"), data={"name": "Test Vendor", "email": "v@t.com"}, follow_redirects=True)
        assert response.status_code == 200
        v = Vendor.query.filter_by(name="Test Vendor").first()
        assert v is not None
        assert v.email == "v@t.com"

    def test_vendor_add_empty_name(self, test_client, db_session):
        login_admin(test_client)
        test_client.post(url_for("shopyo_ecommerce.vendor.add"), data={"name": ""}, follow_redirects=True)
        assert Vendor.query.count() == 0

    def test_vendor_edit(self, test_client, db_session):
        login_admin(test_client)
        v = Vendor(name="Old Name").insert()
        test_client.post(url_for("shopyo_ecommerce.vendor.edit", vendor_id=v.id), data={"name": "Updated Name"}, follow_redirects=True)
        assert Vendor.query.get(v.id).name == "Updated Name"

    def test_vendor_delete(self, test_client, db_session):
        login_admin(test_client)
        v = Vendor(name="Delete Me").insert()
        test_client.post(url_for("shopyo_ecommerce.vendor.delete", vendor_id=v.id), follow_redirects=True)
        assert Vendor.query.get(v.id) is None

    def test_vendor_list(self, test_client, db_session):
        login_admin(test_client)
        Vendor(name="Vendor A").insert()
        Vendor(name="Vendor B").insert()
        response = test_client.get(url_for("shopyo_ecommerce.vendor.dashboard"))
        assert b"Vendor A" in response.data
        assert b"Vendor B" in response.data
