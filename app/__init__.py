from flask import Flask
from dotenv import load_dotenv
import logging

load_dotenv()

def create_app():
    app = Flask(__name__)

    # Logging
    handler = logging.FileHandler('app.log')
    handler.setLevel(logging.INFO)
    app.logger.addHandler(handler)

    app.logger.info("Starting Gutter Tracker application...")

    # Load configuration
    app.config.from_object('app.config.Config')
    app.logger.info("Configuration loaded.")

    # Warn if APP_PASSWORD is using a weak/default value
    app_password = app.config.get("APP_PASSWORD")
    if not app_password or app_password == "changeme":
        app.logger.warning(
            "APP_PASSWORD is not securely configured (value: %s). Set a strong value in production.",
            repr(app_password)
        )

    # Initialize extensions
    from .extensions import db
    db.init_app(app)
    app.logger.info("Database initialized.")

    # Register blueprints
    from .routes import main as main_blueprint
    app.register_blueprint(main_blueprint)
    app.logger.info("Blueprint registered.")

    with app.app_context():
        db.create_all()
        app.logger.info("Database tables created.")

    app.logger.info("Application creation finished.")
    return app
