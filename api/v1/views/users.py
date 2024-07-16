#!/usr/bin/python3
"""View for user objects that handles all default RESTFul API actions"""
from api.v1.views import app_views
from flask import jsonify, make_response, abort, request
from models import storage
from models.user import User


@app_views.route('/users', strict_slashes=False, methods=['GET'])
def users():
    """Retrieves the list of all User objects: GET /api/v1/amentities"""
    all_users = storage.all(User)
    return jsonify([user.to_dict() for user in all_users.values()])

@app_views.route('/users/<user_id>', strict_slashes=False, methods=['GET'])
def get_user(user_id):
    """Retrieves a user object: GET /api/v1/users/<user_id>"""
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    return jsonify(user.to_dict())


@app_views.route('/users/<user_id>', strict_slashes=False,
                 methods=['DELETE'])
def del_user(user_id):
    """Deletes a User object:: DELETE /api/v1/users/<user_id>"""
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    user.delete()
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/users', strict_slashes=False, methods=['POST'])
def post_user():
    """Creates a User: POST /api/v1/users"""
    new_user = request.get_json(silent=True)
    if not request.is_json:
        abort(400, "Not a JSON")
    if "email" not in new_user:
        abort(400, "Missing email")
    if "password" not in new_user:
        abort(400, "Missing password")
    user = User(**new_user)
    storage.new(user)
    storage.save()
    return make_response(jsonify(user.to_dict()), 201)


@app_views.route('/users/<user_id>', strict_slashes=False,
                 methods=['PUT'])
def put_user(user_id):
    """Updates a User object: PUT /api/v1/users/<user_id>"""
    user = storage.get(User, user_id)
    if not user:
        abort(404)

    body_req = request.get_json(silent=True)
    if not request.is_json:
        abort(400, "Not a JSON")

    for key, val in body_req.items():
        if (key != 'id' and key != 'email' and key != 'created_at'
                and key != 'updated_at'):
            setattr(user, key, val)

    storage.save()
    return make_response(jsonify(user.to_dict()), 200)
