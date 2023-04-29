#!/usr/bin/python3
"""start flask server
"""

from flask import Flask
from models import storage
from api.v1.views import app_views
import os

app = Flask(__name__)

app.register_blueprint(app_views)


@app.teardown_appcontext
def clean(exc):
    """close session after each request"""
    storage.close()


if __name__ == "__main__":
    env_host = os.getenv('HBNB_API_HOST')
    env_port = os.getenv('HBNB_API_PORT')
    host = env_host if env_host else '0.0.0.0'
    port = env_port if env_port else 5000
    app.run(host=host, port=port, threaded=True)
