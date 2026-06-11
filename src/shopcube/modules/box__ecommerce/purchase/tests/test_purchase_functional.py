import pytest
from flask import url_for
from modules.box__ecommerce.purchase.models import PurchaseOrder, PurchaseOrderItem
from modules.box__ecommerce.vendor.models import Vendor
from modules.box__ecommerce.category.models import Category, SubCategory
from modules.box__ecommerce.product.models import Product


class TestPurchaseAccess:
    def test_requires_login(self, test_client):
        response = test_client.get("/purchase/dashboard", follow_redirects=True)
        assert response.status_code == 200

    def test_dashboard_admin(self, test_client, login_admin_user):
        response = test_client.get(url_for("purchase.dashboard"))
        assert response.status_code == 200


class TestPurchaseLifecycle:
    def test_create_draft_po(self, test_client, login_admin_user, db_session):
        v = Vendor(name="PO Vendor")
        db_session.add(v)
        db_session.commit()
        response = test_client.post(
            url_for("purchase.add"),
            data={"vendor_id": v.id, "notes": "Test PO"},
            follow_redirects=True,
        )
        assert response.status_code == 200
        po = PurchaseOrder.query.first()
        assert po is not None
        assert po.status == "draft"
        assert po.vendor_id == v.id

    def test_add_item_to_po(self, test_client, login_admin_user, db_session):
        cat = Category(name="pocat")
        cat.save()
        sub = SubCategory(name="posub", category=cat)
        db_session.add(sub)
        db_session.flush()
        prod = Product(barcode="PO001", name="PO Product", selling_price=10, in_stock=5, subcategory_id=sub.id)
        db_session.add(prod)
        db_session.commit()
        po = PurchaseOrder(notes="PO with items")
        po.insert()
        response = test_client.post(
            url_for("purchase.add_item", po_id=po.id),
            data={"barcode": "PO001", "quantity": 10},
            follow_redirects=True,
        )
        assert response.status_code == 200
        po = PurchaseOrder.query.get(po.id)
        assert len(po.items) == 1
        assert po.items[0].product_barcode == "PO001"
        assert po.items[0].quantity_ordered == 10

    def test_place_order(self, test_client, login_admin_user, db_session):
        cat = Category(name="pocat2")
        cat.save()
        sub = SubCategory(name="posub2", category=cat)
        db_session.add(sub)
        db_session.flush()
        prod = Product(barcode="PO002", name="PO Product 2", selling_price=10, in_stock=5, subcategory_id=sub.id)
        db_session.add(prod)
        db_session.commit()
        po = PurchaseOrder(notes="To order")
        po.insert()
        po.items.append(PurchaseOrderItem(product_barcode="PO002", product_name="PO Product 2", quantity_ordered=10, unit_price=5))
        po.update()
        response = test_client.post(url_for("purchase.place_order", po_id=po.id), follow_redirects=True)
        assert response.status_code == 200
        po = PurchaseOrder.query.get(po.id)
        assert po.status == "ordered"

    def test_receive_order(self, test_client, login_admin_user, db_session):
        cat = Category(name="pocat3")
        cat.save()
        sub = SubCategory(name="posub3", category=cat)
        db_session.add(sub)
        db_session.flush()
        prod = Product(barcode="PO003", name="PO Product 3", selling_price=10, in_stock=5, subcategory_id=sub.id)
        db_session.add(prod)
        db_session.commit()
        po = PurchaseOrder(notes="To receive", status="ordered")
        po.insert()
        po.items.append(PurchaseOrderItem(product_barcode="PO003", product_name="PO Product 3", quantity_ordered=10, unit_price=5))
        po.update()
        response = test_client.post(
            url_for("purchase.receive", po_id=po.id),
            data={f"qty_received_{po.items[0].id}": 10},
            follow_redirects=True,
        )
        assert response.status_code == 200
        po = PurchaseOrder.query.get(po.id)
        assert po.status == "received"
        prod = Product.query.filter_by(barcode="PO003").first()
        assert prod.in_stock == 15
