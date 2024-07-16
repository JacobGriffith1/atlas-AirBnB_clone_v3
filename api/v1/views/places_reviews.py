#!/usr/bin/python3
"""View for Place objects that handles all default RESTFul API actions"""
from api.v1.views import app_views
from flask import jsonify, make_response, abort, request
from models import storage
from models.place import Place
from models.review import Review


@app_views.route('/places/<place_id>/reviews', strict_slashes=False, methods=['GET'])
def get_reviews_by_place(place_id):
    """Retrieves the list of all Review objects of a Place: GET /api/v1/places/<place_id>/reviews"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    
    reviews = place.reviews
    reviews_dict = [review.to_dict() for review in reviews ]
    return jsonify(reviews_dict)

@app_views.route('/reviews/<review_id>', strict_slashes=False, methods=['GET'])
def get_review(review_id):
    """Retrieves a Review object: GET /api/v1/reviews/<review_id>"""
    review = storage.get(Review, review_id)
    if not review:
        abort(404)
    return jsonify(review.to_dict())


@app_views.route('/reviews/<review_id>', strict_slashes=False,
                 methods=['DELETE'])
def del_review(review_id):
    """Deletes a Review object:: DELETE /api/v1/reviews/<review_id>"""
    review = storage.get(Review, review_id)
    if not review:
        abort(404)
    review.delete()
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/places/<place_id>/reviews', strict_slashes=False, methods=['POST'])
def post_review(place_id):
    """Creates a Review object: POST /api/v1/places/<place_id>/reviews"""
    new_review = request.get_json(silent=True)
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    if not request.is_json:
        abort(400, "Not a JSON")
    if "user_id" not in new_review:
        abort(400, "Missing user_id")
    user = storage.get(Review, new_review["user_id"])
    if not user:
        abort(404)
    if "text" not in new_review:
        abort(400, "Missing text")
    review = Review(**new_review, place_id=place_id)
    storage.new(review)
    storage.save()
    return make_response(jsonify(review.to_dict()), 201)


@app_views.route('/reviews/<review_id>', strict_slashes=False,
                 methods=['PUT'])
def put_review(review_id):
    """Updates a Review object: PUT /api/v1/reviews/<review_id>"""
    review = storage.get(Review, review_id)
    if not review:
        abort(404)

    body_req = request.get_json(silent=True)
    if not request.is_json:
        abort(400, "Not a JSON")

    for key, val in body_req.items():
        if key != 'id' and key != 'user_id' and key != 'place_id' and key != 'created_at' and key != 'updated_at':
            setattr(review, key, val)

    storage.save()
    return make_response(jsonify(review.to_dict()), 200)
