#!/usr/bin/python3
"""define views of Place objects that handles all defualt
    RESTFul API actions
"""

from api.v1.views import app_views
from models.place import Place
from models.city import City
from models.user import User
from flask import jsonify, abort, request, make_response
from models import storage


@app_views.route('/cities/<city_id>/places', methods=['GET'],
                 strict_slashes=False)
def get_places(city_id):
    """retrieves list of all Place objects of a City"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    places = city.places
    places_json = []
    for place in places:
        places_json.append(place.to_dict())
    return jsonify(places_json)


@app_views.route('/places/<place_id>', methods=['GET'],
                 strict_slashes=False)
def get_place(place_id):
    """retrieves a Place object"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route('/places/<place_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_place(place_id):
    """delete a Place object"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    storage.delete(place)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/cities/<city_id>/places', methods=['POST'],
                 strict_slashes=False)
def create_place(city_id):
    """creates a Place object"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    try:
        data = request.get_json()
    except Exception:
        return make_response("Not a JSON", 400)
    if not data.get('user_id'):
        return make_response("Missing user_id", 400)
    if storage.get(User, data.get('user_id')) is None:
        abort(404)
    if not data.get('name'):
        return make_response("Missing name", 400)
    data['city_id'] = city_id
    new = Place(**data)
    new.save()
    return make_response(jsonify(new.to_dict()), 201)


@app_views.route('/places/<place_id>', methods=['PUT'],
                 strict_slashes=False)
def update_place(place_id):
    """update Place object"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    try:
        data = request.get_json()
    except Exception:
        return make_response("Not a JSON", 400)
    for key, value in data.items():
        if key not in ['id', 'user_id', 'city_id', 'created_at', 'updated_at']:
            setattr(place, key, value)
    storage.save()
    return make_response(jsonify(place.to_dict()), 200)
