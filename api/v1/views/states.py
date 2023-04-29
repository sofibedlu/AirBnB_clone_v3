#!/usr/bin/python3
"""define views for State"""

from api.v1.views import app_views
from models.state import State
from flask import jsonify, abort, request, make_response
from models import storage


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def states_all():
    """retrieves the list of all State objects"""
    states = storage.all(State)
    states_list = []
    for state in states.values():
        states_list.append(state.to_dict())
    return jsonify(states_list)


@app_views.route('/states/<state_id>', methods=['GET', 'DELETE'],
                 strict_slashes=False)
def state_with_id(state_id):
    """retrieves or delete a State object"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    if request.method == 'GET':
        return jsonify(state.to_dict())
    elif request.method == 'DELETE':
        storage.delete(state)
        storage.save()
        return make_response(jsonify({}), 200)


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def create():
    """create a State"""
    try:
        data = request.get_json()
    except Exception as e:
        abort(400, "Not a JSON")
    if not data.get('name'):
        abort(400, "Missing name")
    new = State(name=data["name"])
    new.save()
    return make_response(jsonify(new.to_dict()), 201)


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def update(state_id):
    """updates a State object"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    try:
        data = request.get_json()
    except Exception as e:
        abort(400, "Not a JSON")
    for key, value in data.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(state, key, value)
    storage.save()
    return make_response(jsonify(state.to_dict()), 200)
