#!/usr/bin/python3
"""View for Place objects that handles all default RESTFul API actions"""
from api.v1.views import app_views
from flask import jsonify, make_response, abort, request
from models import storage
from models.place import Place
from models.city import City


@app_views.route('/cities/<city_id>/places', strict_slashes=False,
                 methods=['GET'])
def get_place_by_city(city_id):
    """
    Retrieves the list of all Place objects of a City:
    GET /api/v1/cities/<city_id>/places
    """
    city = storage.get(City, city_id)
    if not city:
        abort(404)

    places = city.places
    places_dict = [place.to_dict() for place in places ]
    return jsonify(places_dict)


@app_views.route('/places/<place_id>', strict_slashes=False, methods=['GET'])
def get_place(place_id):
    """Retrieves a Place object: GET /api/v1/places/<place_id>"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route('/places/<place_id>', strict_slashes=False,
                 methods=['DELETE'])
def del_place(place_id):
    """Deletes a Place object:: DELETE /api/v1/places/<place_id>"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    place.delete()
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/cities/<city_id>/places', strict_slashes=False,
                 methods=['POST'])
def post_place(city_id):
    """Creates a Place object: POST /api/v1/cities/<city_id>/places"""
    new_place = request.get_json(silent=True)
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    if not request.is_json:
        abort(400, "Not a JSON")
    if "user_id" not in new_place:
        abort(400, "Missing user_id")
    user = storage.get(Place, new_place["user_id"])
    if not user:
        abort(404)
    if "name" not in new_place:
        abort(400, "Missing name")
    place = Place(**new_place, city_id=city_id)
    storage.new(place)
    storage.save()
    return make_response(jsonify(place.to_dict()), 201)


@app_views.route('/places/<place_id>', strict_slashes=False,
                 methods=['PUT'])
def put_place(place_id):
    """Updates a Place object: PUT /api/v1/places/<place_id>"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)

    body_req = request.get_json(silent=True)
    if not request.is_json:
        abort(400, "Not a JSON")

    for key, val in body_req.items():
        if (key != 'id' and key != 'user_id' and key != 'city_id'
                and key != 'created_at' and key != 'updated_at'):
            setattr(place, key, val)

    storage.save()
    return make_response(jsonify(place.to_dict()), 200)
