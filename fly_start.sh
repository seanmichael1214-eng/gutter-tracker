#!/bin/bash
set -e

echo "🚀 Starting Gutter Tracker on Fly.io..."

# Initialize database tables
echo "📦 Initializing database..."
python3 - << 'PYTHON'
from app import create_app
app = create_app()
with app.app_context():
    from app.extensions import db
    try:
        db.create_all()
        print("✅ Database tables initialized")
    except Exception as e:
        print(f"⚠️ Database initialization: {e}")
        print("Tables may already exist - continuing...")
PYTHON

echo "🌐 Starting web server on port ${PORT:-8080}..."
exec gunicorn run:app --bind 0.0.0.0:${PORT:-8080} --workers 2 --threads 2 --timeout 120
