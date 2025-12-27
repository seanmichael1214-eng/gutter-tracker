#!/bin/bash
# Initialize database tables if they don't exist
python3 - << 'PY'
from app import create_app
app = create_app()
with app.app_context():
    from app.extensions import db
    db.create_all()
    print("✅ Database tables initialized")
PY

# Start the application
gunicorn run:app --bind 0.0.0.0:$PORT
