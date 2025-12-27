import os
import sys

# Add the project root to the python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app import create_app
from app.extensions import db
import os

app = create_app()

# Ensure the instance directory exists for SQLite storage
instance_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "instance"))
os.makedirs(instance_dir, exist_ok=True)

with app.app_context():
    db.create_all()
    print("Database initialized!")
