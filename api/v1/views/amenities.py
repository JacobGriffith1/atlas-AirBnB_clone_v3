#!/usr/bin/python3
"""View for Amenity objects that handles all default RESTFul API actions"""
from api.v1.views import app_views
from flask import jsonify, make_response, abort, request
from models import storage
from models.amenity import Amenity


@app_views.route('/amenities', strict_slashes=False, methods=['GET'])
def amenities():
    """Retrieves the list of all Amenity objects: GET /api/v1/amentities"""
    all_amenities = storage.all(Amenity)
    return jsonify([amenity.to_dict() for amenity in all_amenities.values()])


@app_views.route('/amenities/<amenity_id>', strict_slashes=False, methods=['GET'])
def get_amenity(amenity_id):
    """Retrieves an Amenity object: GET /api/v1/amenities/<amenity_id>"""
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    return jsonify(amenity.to_dict())


@app_views.route('/amenities/<amenity_id>', strict_slashes=False,
                 methods=['DELETE'])
def del_amenity(amenity_id):
    """Deletes an Amenity object:: DELETE /api/v1/amenities/<amenity_id>"""
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    amenity.delete()
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/amenities', strict_slashes=False, methods=['POST'])
def post_amenity():
    """Creates an Amenity: POST /api/v1/amenities"""
    new_amenity = request.get_json()
    if not new_amenity:
        abort(400, "Not a JSON")
    if "name" not in new_amenity:
        abort(400, "Missing name")
    amenity = Amenity(**new_amenity)
    storage.new(amenity)
    storage.save()
    return make_response(jsonify(amenity.to_dict()), 201)


@app_views.route('/amenities/<amenity_id>', strict_slashes=False,
                 methods=['PUT'])
def put_amenity(amenity_id):
    """Updates an Amenity object: PUT /api/v1/amenities/<amenity_id>"""
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)

    body_req = request.get_json()
    if not body_req:
        abort(400, "Not a JSON")

    for key, val in body_req.items():
        if key != 'id' and key != 'created_at' and key != 'updated_at':
            setattr(amenity, key, val)

    storage.save()
    return make_response(jsonify(amenity.to_dict()), 200)
