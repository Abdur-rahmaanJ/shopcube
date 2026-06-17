import pytest
from app import create_app
from init import db


@pytest.fixture(scope="session")
def app():
    # Import Resource model so it's registered with SQLAlchemy before
    # models that reference it via string-based relationships.
    import modules.resource.models  # noqa: F401

    _app = create_app("testing")
    with _app.app_context():
        db.create_all()
        yield _app
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()
