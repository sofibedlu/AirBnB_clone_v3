#!/usr/bin/python3
"""defines views/endpoints
"""
from api.v1.views import app_views
from flask import jsonify
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User

classes = {"amenities": Amenity, "cities": City,
           "places": Place, "reviews": Review, "states": State, "users": User}


@app_views.route('/status', strict_slashes=False)
def index():
    data = {"status": "OK"}
    return jsonify(data)


@app_views.route('/stats', strict_slashes=False)
def num_objs():
    """retrieves the number of each objects by type
    """
    data = {}
    from models import storage
    for key, cls in classes.items():
        data[key] = storage.count(cls)
    return jsonify(data)
