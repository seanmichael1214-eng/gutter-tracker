from flask import Flask
import pytest

# Create a fixture for the app
@pytest.fixture
def app():
    app = Flask(__name__)

    @app.route("/")
    def hello():
        return """
        <html>
        <head><title>Test</title></head>
        <body style="font-family: Arial; padding: 50px; text-align: center;">
            <h1>✅ Flask is Working!</h1>
            <p>If you can see this, Flask is running correctly.</p>
            <p><a href="/test">Click here for another test</a></p>
        </body>
        </html>
        """

    @app.route("/test")
    def test_route():
        return '<h1>✅ Routes work!</h1><p><a href="/">Go back</a></p>'
    
    return app

# Create a fixture for the client
@pytest.fixture
def client(app):
    return app.test_client()

def test_hello_route(client):
    """Test the / route."""
    response = client.get("/")
    assert response.status_code == 200
    assert b"Flask is Working!" in response.data

def test_test_route(client):
    """Test the /test route."""
    response = client.get("/test")
    assert response.status_code == 200
    assert b"Routes work!" in response.data