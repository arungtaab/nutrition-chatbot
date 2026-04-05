"""WSGI entry for production servers (gunicorn, etc.)."""
from app import app

application = app
