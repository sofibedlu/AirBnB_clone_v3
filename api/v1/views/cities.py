#!/usr/bin/python3
"""define views for City"""

from api.v1.views import app_views
from models.city import City
from models.state import State
from flask import jsonify, abort, request, make_response
from models import storage


@app_views.route('/states/<state_id>/cities', methods=['GET'],
                 strict_slashes=False)
def state_cities(state_id):
    """retrieves the list of all City objects
        of a State
    """
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    cities = state.cities
    cities_json = []
    for citie in cities:
        cities_json.append(citie.to_dict())
    return jsonify(cities_json)


@app_views.route('/cities/<city_id>', methods=['GET', 'DELETE'],
                 strict_slashes=False)
def city_obj(city_id):
    """retrieves a City object"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    if request.method == 'GET':
        return jsonify(city.to_dict())
    elif request.method == 'DELETE':
        storage.delete(city)
        storage.save()
        return make_response(jsonify({}), 200)


@app_views.route('/states/<state_id>/cities', methods=['POST'],
                 strict_slashes=False)
def create_city(state_id):
    """creates a City object"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    if not request.is_json:
        abort(400, "Not a JSON")
    try:
        data = request.get_json()
    except ValueError:
        return make_response("Not a JSON\n", 400)
    if not data.get('name'):
        return make_response("Missing name\n", 400)
    new = City(name=data.get('name'), state_id=state_id)
    new.save()
    return make_response(jsonify(new.to_dict()), 201)


@app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
def update_city(city_id):
    """update a City object"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    if not request.is_json:
        abort(400, "Not a JSON")
    try:
        data = request.get_json()
    except ValueError:
        return make_response("Not a JSON\n", 400)
    for key, value in data.items():
        if key not in ['id', 'created_at', 'updated_at', 'state_id']:
            setattr(city, key, value)
    storage.save()
    return make_response(jsonify(city.to_dict()), 200)
