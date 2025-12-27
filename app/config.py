import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key-change-in-production")
    
    # Handle both SQLite and PostgreSQL URLs
    database_url = os.getenv("DATABASE_URL", "sqlite:///../instance/gutter_tracker.db")
    # Vercel Postgres uses postgres:// but SQLAlchemy needs postgresql://
    if database_url.startswith("postgres://"):
        database_url = database_url.replace("postgres://", "postgresql://", 1)
    
    SQLALCHEMY_DATABASE_URI = database_url
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    APP_PASSWORD = os.getenv("APP_PASSWORD", "nao$")
