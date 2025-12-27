import pytest
from app import create_app
from app.extensions import db


@pytest.fixture(scope='module')
def app():
    """
    Creates a test Flask app context.
    """
    app = create_app({
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:',
        'WTF_CSRF_ENABLED': False,
        'APP_PASSWORD': 'NAO$',
    })
    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()

@pytest.fixture()
def client(app):
    """
    Creates a test client for the app.
    """
    return app.test_client()
