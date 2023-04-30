#!/usr/bin/python3
"""define views of Amenity
"""

from api.v1.views import app_views
from models.amenity import Amenity
from flask import jsonify, abort, request, make_response
from models import storage


@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
def get_amenities():
    """retrieves list of all Amenity objects"""
    amenities = storage.all(Amenity)
    amenities_json = []
    for amenity in amenities.values():
        amenities_json.append(amenity.to_dict())
    return jsonify(amenities_json)


@app_views.route('/amenities/<amenity_id>', methods=['GET', 'DELETE'],
                 strict_slashes=False)
def get_amenity(amenity_id):
    """retrieves a Amenity object"""
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    if request.method == 'GET':
        return jsonify(amenity.to_dict())
    elif request.method == 'DELETE':
        storage.delete(amenity)
        storage.save()
        return make_response({}, 200)


@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def create_amenity():
    """creates a Amenity"""
    try:
        data = request.get_json()
    except Exception:
        return make_response("Not a JSON", 400)
    if not data.get('name'):
        return make_response("Missing name", 400)
    new = Amenity(name=data.get('name'))
    new.save()
    return make_response(jsonify(new.to_dict()), 201)


@app_views.route('/amenities/<amenity_id>', methods=['PUT'],
                 strict_slashes=False)
def update_amenity(amenity_id):
    """update Amenity object"""
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    try:
        data = request.get_json()
    except Exception:
        return make_response("Not a JSON", 400)
    for key, value in data.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(amenity, key, value)
    return make_response(jsonify(amenity.to_dict()), 200)
