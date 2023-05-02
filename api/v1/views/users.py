#!/usr/bin/python3
"""define views of User
"""

from api.v1.views import app_views
from models.user import User
from flask import jsonify, abort, request, make_response
from models import storage


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def get_users():
    """retrieves list of all User objects"""
    users = storage.all(User)
    users_json = []
    for user in users.values():
        users_json.append(user.to_dict())
    return jsonify(users_json)


@app_views.route('/users/<user_id>', methods=['GET'],
                 strict_slashes=False)
def get_user(user_id):
    """retrieves a User object"""
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    return jsonify(user.to_dict())


@app_views.route('/users/<user_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_user(user_id):
    """delete a User object"""
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    storage.delete(user)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def create_user():
    """creates a User object"""
    if not request.is_json:
        abort(400, "Not a JSON")
    try:
        data = request.get_json()
    except ValueError:
        return make_response("Not a JSON", 400)
    if not data.get('email'):
        return make_response("Missing email", 400)
    if not data.get('password'):
        return make_response("Missing password", 400)
    new = User(**data)
    new.save()
    return make_response(jsonify(new.to_dict()), 201)


@app_views.route('/users/<user_id>', methods=['PUT'],
                 strict_slashes=False)
def update_user(user_id):
    """update User object"""
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    if not request.is_json:
        abort(400, "Not a JSON")
    try:
        data = request.get_json()
    except ValueError:
        return make_response("Not a JSON", 400)
    for key, value in data.items():
        if key not in ['id', 'created_at', 'updated_at', 'email']:
            setattr(user, key, value)
    storage.save()
    return make_response(jsonify(user.to_dict()), 200)
