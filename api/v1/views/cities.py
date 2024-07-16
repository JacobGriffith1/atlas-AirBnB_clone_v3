#!/usr/bin/python3
"""View for City objects that handles all default RESTFul API actions"""
from api.v1.views import app_views
from flask import jsonify, make_response, abort, request
from models import storage
from models.city import City
from models.state import State


@app_views.route('/states/<state_id>/cities', strict_slashes=False,
                 methods=['GET'])
def get_cities_by_state(state_id):
    """
    Retrieves the list of all City objects of a State:
    GET /api/v1/states/<state_id>/cities
    """
    state = storage.get(State, state_id)

    if not state:
        abort(404)

    cities = state.cities
    cities_dict = [city.to_dict() for city in cities]
    return jsonify(cities_dict)


@app_views.route('/cities/<city_id>', strict_slashes=False, methods=['GET'])
def get_city(city_id):
    """Retrieves a City object: GET /api/v1/cities/<city_id>"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    return jsonify(city.to_dict())


@app_views.route('/cities/<city_id>', strict_slashes=False,
                 methods=['DELETE'])
def del_city(city_id):
    """Deletes a City object:: DELETE /api/v1/cities/<City_id>"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    city.delete()
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/states/<state_id>/cities', strict_slashes=False,
                 methods=['POST'])
def post_city(state_id):
    """Creates a City: POST /api/v1/cities"""
    new_city = request.get_json(silent=True)
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    if not request.is_json:
        abort(400, "Not a JSON")
    if "name" not in new_city:
        abort(400, "Missing name")
    city = City(**new_city, state_id=state_id)
    storage.new(city)
    storage.save()
    return make_response(jsonify(city.to_dict()), 201)


@app_views.route('/cities/<city_id>', strict_slashes=False,
                 methods=['PUT'])
def put_city(city_id):
    """Updates a City object: PUT /api/v1/cities/<city_id>"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)

    body_req = request.get_json(silent=True)
    if not request.is_json:
        abort(400, "Not a JSON")

    for key, val in body_req.items():
        if (key != 'id' and key != 'state_id' and key != 'created_at'
            and key != 'updated_at'):
            setattr(city, key, val)

    storage.save()
    return make_response(jsonify(city.to_dict()), 200)
