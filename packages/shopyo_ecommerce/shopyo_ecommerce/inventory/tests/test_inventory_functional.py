import pytest
from flask import url_for
from shopyo_ecommerce.inventory.models import InventoryCount, InventoryCountItem, Location, StockTransfer, StockTransferItem
from shopyo_ecommerce.category.models import Category, SubCategory
from shopyo_ecommerce.product.models import Product


class TestInventoryAccess:
    def test_requires_login(self, test_client):
        from flask import url_for
        response = test_client.get(url_for("shopyo_ecommerce.inventory.dashboard"), follow_redirects=True)
        assert response.status_code == 200

    def test_dashboard_admin(self, test_client, login_admin_user):
        response = test_client.get(url_for("shopyo_ecommerce.inventory.dashboard"))
        assert response.status_code == 200


class TestInventoryCounts:
    def test_create_count_sheet(self, test_client, login_admin_user, db_session):
        cat = Category(name="iccat")
        cat.save()
        sub = SubCategory(name="icsub", category=cat)
        db_session.add(sub)
        db_session.flush()
        prod = Product(barcode="IC001", name="Count Product", selling_price=10, in_stock=5, subcategory_id=sub.id)
        db_session.add(prod)
        db_session.commit()
        response = test_client.post(url_for("shopyo_ecommerce.inventory.new"), data={"notes": "Test count"}, follow_redirects=True)
        assert response.status_code == 200
        ic = InventoryCount.query.first()
        assert ic is not None
        assert len(ic.items) == 1

    def test_complete_count_adjusts_stock(self, test_client, login_admin_user, db_session):
        cat = Category(name="iccat2")
        cat.save()
        sub = SubCategory(name="icsub2", category=cat)
        db_session.add(sub)
        db_session.flush()
        prod = Product(barcode="IC002", name="Count Product 2", selling_price=10, in_stock=5, subcategory_id=sub.id)
        db_session.add(prod)
        db_session.commit()
        ic = InventoryCount(notes="Adjustment test")
        ic.insert()
        ic.items.append(InventoryCountItem(product_id=prod.id, expected_qty=5, actual_qty=8))
        ic.update()
        response = test_client.post(url_for("shopyo_ecommerce.inventory.count", count_id=ic.id), follow_redirects=True)
        assert response.status_code == 200
        prod = Product.query.get(prod.id)
        assert prod.in_stock == 8


class TestLocations:
    def test_add_location(self, test_client, login_admin_user):
        response = test_client.post(
            url_for("shopyo_ecommerce.inventory.location_add"),
            data={"name": "Warehouse A", "address": "123 Main St"},
            follow_redirects=True,
        )
        assert response.status_code == 200
        loc = Location.query.filter_by(name="Warehouse A").first()
        assert loc is not None
        assert loc.address == "123 Main St"

    def test_delete_location(self, test_client, login_admin_user):
        loc = Location(name="Temp Location").insert()
        response = test_client.post(url_for("shopyo_ecommerce.inventory.location_delete", loc_id=loc.id), follow_redirects=True)
        assert response.status_code == 200
        assert Location.query.get(loc.id) is None


class TestStockTransfers:
    def test_create_transfer(self, test_client, login_admin_user, db_session):
        loc_a = Location(name="Source").insert()
        loc_b = Location(name="Dest").insert()
        response = test_client.post(
            url_for("shopyo_ecommerce.inventory.transfer_create"),
            data={"from_location_id": loc_a.id, "to_location_id": loc_b.id},
            follow_redirects=True,
        )
        assert response.status_code == 200
        t = StockTransfer.query.first()
        assert t is not None
        assert t.from_location_id == loc_a.id
        assert t.to_location_id == loc_b.id
        assert t.status == "draft"

    def test_transfer_complete_deducts_stock(self, test_client, login_admin_user, db_session):
        loc_a = Location(name="Source2").insert()
        loc_b = Location(name="Dest2").insert()
        cat = Category(name="tcat")
        cat.save()
        sub = SubCategory(name="tsub", category=cat)
        db_session.add(sub)
        db_session.flush()
        prod = Product(barcode="TR001", name="Transfer Product", selling_price=10, in_stock=20, subcategory_id=sub.id)
        db_session.add(prod)
        db_session.commit()

        t = StockTransfer(from_location_id=loc_a.id, to_location_id=loc_b.id)
        t.insert()
        t.items.append(StockTransferItem(product_id=prod.id, quantity=5))
        t.update()

        response = test_client.post(url_for("shopyo_ecommerce.inventory.transfer_complete", t_id=t.id), follow_redirects=True)
        assert response.status_code == 200
        prod = Product.query.get(prod.id)
        assert prod.in_stock == 15
