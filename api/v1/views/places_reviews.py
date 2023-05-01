#!/usr/bin/python3
"""define view for Review object that handles all default REASTFul API
    actions
"""

from api.v1.views import app_views
from models.review import Review
from models.place import Place
from models.user import User
from flask import jsonify, abort, request, make_response
from models import storage


@app_views.route('/places/<place_id>/reviews', methods=['GET'],
                 strict_slashes=False)
def get_reviews(place_id):
    """retrieves list of all Review objects of a Place"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    reviews = place.reviews
    review_json = []
    for review in reviews:
        review_json.append(review.to_dict())
    return jsonify(review_json)


@app_views.route('/reviews/<review_id>', methods=['GET'],
                 strict_slashes=False)
def get_review(review_id):
    """retrieves a Review object"""
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    return jsonify(review.to_dict())


@app_views.route('/reviews/<review_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_review(review_id):
    """delete a Review object"""
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    storage.delete(review)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/places/<place_id>/reviews', methods=['POST'],
                 strict_slashes=False)
def create_review(place_id):
    """creates a Review object"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    try:
        data = request.get_json()
    except Exception:
        return make_response("Not a JSON", 400)
    if not data.get('user_id'):
        return make_response("Missing user_id", 400)
    if storage.get(User, data.get('user_id')) is None:
        abort(404)
    if not data.get('text'):
        return make_response("Missing text", 400)
    data['place_id'] = place_id
    new = Review(**data)
    new.save()
    return make_response(jsonify(new.to_dict()), 201)


@app_views.route('/reviews/<review_id>', methods=['PUT'],
                 strict_slashes=False)
def update_review(review_id):
    """update Review object"""
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    try:
        data = request.get_json()
    except Exception:
        return make_response("Not a JSON", 400)
    for key, value in data.items():
        if (key not in ['id', 'created_at', 'updated_at', 'user_id',
                        'place_id']):
            setattr(review, key, value)
    storage.save()
    return make_response(jsonify(review.to_dict()), 200)
