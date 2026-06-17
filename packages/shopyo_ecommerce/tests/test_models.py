from init import db
from shopyo_ecommerce.category.models import Category, SubCategory
from shopyo_ecommerce.customer.models import Customer, CustomerGroup
from shopyo_ecommerce.inventory.models import (
    Location, StockPerLocation, StockTransfer, StockTransferItem,
    InventoryCount, InventoryCountItem,
)
from shopyo_ecommerce.pos.models import Transaction, TransactionItem, Shift, QuickKey
from shopyo_ecommerce.product.models import Product, StockAdjustment, Color, BundleComponent, Size
from shopyo_ecommerce.purchase.models import PurchaseOrder, PurchaseOrderItem
from shopyo_ecommerce.shop.models import Order, OrderItem, BillingDetail
from shopyo_ecommerce.shopman.models import DeliveryOption, PaymentOption, Coupon
from shopyo_ecommerce.vendor.models import Vendor


class TestTableNames:
    def test_category_tablenames(self):
        assert Category.__tablename__ == "shopyo_ecommerce_categories"
        assert SubCategory.__tablename__ == "shopyo_ecommerce_subcategories"

    def test_customer_tablenames(self):
        assert Customer.__tablename__ == "shopyo_ecommerce_customer"
        assert CustomerGroup.__tablename__ == "shopyo_ecommerce_customer_groups"

    def test_inventory_tablenames(self):
        assert Location.__tablename__ == "shopyo_ecommerce_locations"
        assert StockPerLocation.__tablename__ == "shopyo_ecommerce_stock_per_location"
        assert StockTransfer.__tablename__ == "shopyo_ecommerce_stock_transfers"
        assert StockTransferItem.__tablename__ == "shopyo_ecommerce_stock_transfer_items"
        assert InventoryCount.__tablename__ == "shopyo_ecommerce_inventory_counts"
        assert InventoryCountItem.__tablename__ == "shopyo_ecommerce_inventory_count_items"

    def test_pos_tablenames(self):
        assert Transaction.__tablename__ == "shopyo_ecommerce_transactions"
        assert TransactionItem.__tablename__ == "shopyo_ecommerce_transaction_items"
        assert Shift.__tablename__ == "shopyo_ecommerce_shifts"
        assert QuickKey.__tablename__ == "shopyo_ecommerce_quick_keys"

    def test_product_tablenames(self):
        assert Product.__tablename__ == "shopyo_ecommerce_product"
        assert StockAdjustment.__tablename__ == "shopyo_ecommerce_stock_adjustments"
        assert Color.__tablename__ == "shopyo_ecommerce_color"
        assert BundleComponent.__tablename__ == "shopyo_ecommerce_bundle_components"
        assert Size.__tablename__ == "shopyo_ecommerce_size"

    def test_purchase_tablenames(self):
        assert PurchaseOrder.__tablename__ == "shopyo_ecommerce_purchase_orders"
        assert PurchaseOrderItem.__tablename__ == "shopyo_ecommerce_purchase_order_items"

    def test_shop_tablenames(self):
        assert Order.__tablename__ == "shopyo_ecommerce_orders"
        assert OrderItem.__tablename__ == "shopyo_ecommerce_order_items"
        assert BillingDetail.__tablename__ == "shopyo_ecommerce_billing_details"

    def test_shopman_tablenames(self):
        assert DeliveryOption.__tablename__ == "shopyo_ecommerce_deliveryoptions"
        assert PaymentOption.__tablename__ == "shopyo_ecommerce_paymentoptions"
        assert Coupon.__tablename__ == "shopyo_ecommerce_coupons"

    def test_vendor_tablenames(self):
        assert Vendor.__tablename__ == "shopyo_ecommerce_vendors"


class TestModelCRUD:
    def test_create_category(self):
        c = Category(name="testcat")
        c.save()
        assert Category.query.filter_by(name="testcat").first() is not None
        c.delete()

    def test_create_subcategory(self):
        cat = Category(name="catforsub").save()
        sub = SubCategory(name="testsub", category_id=cat.id).save()
        assert SubCategory.query.filter_by(name="testsub").first() is not None
        sub.delete()
        cat.delete()

    def test_create_vendor(self):
        v = Vendor(name="Test Vendor", email="vendor@test.com")
        v.insert()
        assert Vendor.query.filter_by(name="Test Vendor").first() is not None
        db.session.delete(v)
        db.session.commit()

    def test_create_product(self):
        cat = Category(name="catforprod").save()
        sub = SubCategory(name="subforprod", category_id=cat.id).save()
        p = Product(
            barcode="TEST001",
            name="Test Product",
            price=9.99,
            selling_price=14.99,
            in_stock=10,
            subcategory_id=sub.id,
        ).insert()
        assert Product.query.filter_by(barcode="TEST001").first() is not None
        p.delete()
        sub.delete()
        cat.delete()

    def test_create_location(self):
        loc = Location(name="Warehouse A", address="123 Main St")
        loc.insert()
        assert Location.query.filter_by(name="Warehouse A").first() is not None
        loc.delete()

    def test_order_billing_relationship(self):
        o = Order()
        o.insert()
        b = BillingDetail(first_name="John", last_name="Doe", email="john@test.com", order_id=o.id)
        b.insert()
        assert o.billing_detail is not None
        assert o.billing_detail.first_name == "John"
        b.delete()
        o.delete()

    def test_product_colors_sizes(self):
        cat = Category(name="catforvariants").save()
        sub = SubCategory(name="subforvariants", category_id=cat.id).save()
        p = Product(
            barcode="VAR001", name="Variant Product", price=10,
            selling_price=15, in_stock=5, subcategory_id=sub.id,
        ).insert()
        c1 = Color(name="Red", product_id=p.id).save()
        s1 = Size(name="M", product_id=p.id).save()
        assert len(p.colors) == 1
        assert p.colors[0].name == "Red"
        assert len(p.sizes) == 1
        assert p.sizes[0].name == "M"
        c1.delete()
        s1.delete()
        p.delete()
        sub.delete()
        cat.delete()

    def test_vendor_products_relationship(self):
        v = Vendor(name="Rel Vendor").insert()
        cat = Category(name="catforrel").save()
        sub = SubCategory(name="subforrel", category_id=cat.id).save()
        p = Product(
            barcode="REL001", name="Rel Product", price=5,
            selling_price=8, in_stock=2, subcategory_id=sub.id, vendor_id=v.id,
        ).insert()
        assert p.vendor is not None
        assert p.vendor.name == "Rel Vendor"
        p.delete()
        sub.delete()
        cat.delete()
        v.delete()
