#!/usr/bin/python3
"""defines views/endpoints
"""
from api.v1.views import app_views
from flask import jsonify


@app_views.route('/status', strict_slashes=False)
def index():
    data = {"status": "OK"}
    return jsonify(data)
