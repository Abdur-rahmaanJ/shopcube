import pytest
from app import create_app
from init import db


@pytest.fixture(scope="session")
def app():
    # Import all models so SQLAlchemy can resolve string-based relationships
    import shopyo_ecommerce.resource.models  # noqa: F401
    import shopyo_ecommerce.product.models  # noqa: F401
    import shopyo_ecommerce.category.models  # noqa: F401
    import shopyo_ecommerce.vendor.models  # noqa: F401
    import shopyo_ecommerce.customer.models  # noqa: F401
    import shopyo_ecommerce.inventory.models  # noqa: F401
    import shopyo_ecommerce.pos.models  # noqa: F401
    import shopyo_ecommerce.purchase.models  # noqa: F401
    import shopyo_ecommerce.shop.models  # noqa: F401
    import shopyo_ecommerce.shopman.models  # noqa: F401

    _app = create_app("testing")
    with _app.app_context():
        db.create_all()
        yield _app
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()
