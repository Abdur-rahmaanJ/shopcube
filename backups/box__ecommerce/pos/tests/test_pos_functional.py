import pytest
from flask import url_for
from modules.box__ecommerce.pos.models import Transaction, TransactionItem, Shift, QuickKey
from modules.box__ecommerce.category.models import Category, SubCategory
from modules.box__ecommerce.product.models import Product


def login_admin(test_client):
    test_client.post(url_for("shopyo_auth.login"), data=dict(email="admin2@domain.com", password="pass"), follow_redirects=True)
    return test_client


class TestPosTransaction:
    def test_transaction_empty_items_allowed(self, test_client, db_session):
        login_admin(test_client)
        response = test_client.post(url_for("pos.transaction"), json={"items": {}, "amount_paid": 10})
        assert response.status_code == 200
        data = response.get_json()
        assert data["success"] is True

    def test_transaction_invalid_product(self, test_client, db_session):
        login_admin(test_client)
        response = test_client.post(url_for("pos.transaction"), json={"items": {"NONEXISTENT": {"count": 1}}, "amount_paid": 10})
        assert response.status_code == 400
        data = response.get_json()
        assert "Product not found" in data["message"]

    def test_transaction_success(self, test_client, db_session):
        login_admin(test_client)
        cat = Category(name="tcat1")
        cat.save()
        sub = SubCategory(name="tsub1", category=cat)
        db_session.add(sub)
        db_session.flush()
        prod = Product(barcode="T001", name="Test", selling_price=10, in_stock=5, subcategory_id=sub.id)
        db_session.add(prod)
        db_session.commit()
        response = test_client.post(url_for("pos.transaction"), json={"items": {"T001": {"count": 2}}, "amount_paid": 25})
        assert response.status_code == 200
        data = response.get_json()
        assert data["success"] is True
        prod = Product.query.filter_by(barcode="T001").first()
        assert prod.in_stock == 3

    def test_transaction_insufficient_payment(self, test_client, db_session):
        login_admin(test_client)
        cat = Category(name="tcat2")
        cat.save()
        sub = SubCategory(name="tsub2", category=cat)
        db_session.add(sub)
        db_session.flush()
        prod = Product(barcode="T002", name="Test2", selling_price=15, in_stock=5, subcategory_id=sub.id)
        db_session.add(prod)
        db_session.commit()
        response = test_client.post(url_for("pos.transaction"), json={"items": {"T002": {"count": 3}}, "amount_paid": 10})
        assert response.status_code == 400
        assert "Insufficient payment" in response.get_json()["message"]

    def test_transaction_with_discount(self, test_client, db_session):
        login_admin(test_client)
        cat = Category(name="tcat3")
        cat.save()
        sub = SubCategory(name="tsub3", category=cat)
        db_session.add(sub)
        db_session.flush()
        prod = Product(barcode="T003", name="Test3", selling_price=100, in_stock=10, subcategory_id=sub.id)
        db_session.add(prod)
        db_session.commit()
        response = test_client.post(url_for("pos.transaction"), json={"items": {"T003": {"count": 2}}, "amount_paid": 200, "discount_type": "percentage", "discount_value": 10})
        assert response.status_code == 200
        tx = Transaction.query.first()
        assert tx.discount_type == "percentage"
        assert float(tx.discount_value) == 10

    def test_transaction_with_notes(self, test_client, db_session):
        login_admin(test_client)
        cat = Category(name="tcat4")
        cat.save()
        sub = SubCategory(name="tsub4", category=cat)
        db_session.add(sub)
        db_session.flush()
        prod = Product(barcode="T004", name="Test4", selling_price=10, in_stock=5, subcategory_id=sub.id)
        db_session.add(prod)
        db_session.commit()
        response = test_client.post(url_for("pos.transaction"), json={"items": {"T004": {"count": 1}}, "amount_paid": 10, "notes": "Test note"})
        assert response.status_code == 200
        tx = Transaction.query.first()
        assert tx.notes == "Test note"


class TestPosShifts:
    def test_shift_open_close(self, test_client, db_session):
        login_admin(test_client)
        response = test_client.post(url_for("pos.shift_open"), data={"starting_cash": 100}, follow_redirects=True)
        assert response.status_code == 200
        s = Shift.query.filter_by(status="open").first()
        assert s is not None
        assert float(s.starting_cash) == 100
        test_client.post(url_for("pos.shift_close", shift_id=s.id), data={"actual_cash": 500}, follow_redirects=True)
        s = Shift.query.get(s.id)
        assert s.status == "closed"

    def test_shift_double_open_denied(self, test_client, db_session):
        login_admin(test_client)
        test_client.post(url_for("pos.shift_open"), data={"starting_cash": 0}, follow_redirects=True)
        response = test_client.post(url_for("pos.shift_open"), data={"starting_cash": 0}, follow_redirects=True)
        assert response.status_code == 200
        assert Shift.query.filter_by(status="open").count() == 1


class TestPosQuickKeys:
    def test_quick_key_add_delete(self, test_client, db_session):
        login_admin(test_client)
        cat = Category(name="qcat")
        cat.save()
        sub = SubCategory(name="qsub", category=cat)
        db_session.add(sub)
        db_session.flush()
        prod = Product(barcode="Q001", name="QK", selling_price=5, in_stock=10, subcategory_id=sub.id)
        db_session.add(prod)
        db_session.commit()
        response = test_client.post(url_for("pos.quick_key_add"), data={"product_id": prod.id, "position": 1, "label": "Q1"}, follow_redirects=True)
        assert response.status_code == 200
        qk = QuickKey.query.first()
        assert qk is not None
        assert qk.position == 1
        test_client.post(url_for("pos.quick_key_delete", key_id=qk.id), follow_redirects=True)
        assert QuickKey.query.count() == 0


class TestPosReturns:
    def test_return_process(self, test_client, db_session):
        login_admin(test_client)
        cat = Category(name="rcat")
        cat.save()
        sub = SubCategory(name="rsub", category=cat)
        db_session.add(sub)
        db_session.flush()
        prod = Product(barcode="R001", name="Ret", selling_price=20, in_stock=5, subcategory_id=sub.id)
        db_session.add(prod)
        db_session.commit()
        tx = Transaction(total_amount=40, method_of_payment="cash", cashier_id=1)
        tx.insert()
        db_session.add(TransactionItem(transaction_id=tx.id, product_barcode="R001", quantity=2, unit_price=20))
        db_session.commit()
        response = test_client.post(url_for("pos.process_return", tx_id=tx.id), follow_redirects=True)
        assert response.status_code == 200
        prod = Product.query.filter_by(barcode="R001").first()
        assert prod.in_stock == 7
