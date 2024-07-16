#!/usr/bin/python3
"""View for State objects that handles all default RESTFul API actions"""
from api.v1.views import app_views
from flask import jsonify, make_response, abort, request
from models import storage
from models.state import State


@app_views.route('/states', strict_slashes=False, methods=['GET'])
def states():
    """Retrieves the list of all State objects: GET /api/v1/states"""
    all_states = storage.all(State)
    return jsonify([obj.to_dict() for obj in all_states.values()])


@app_views.route('/states/<state_id>', strict_slashes=False, methods=['GET'])
def get_state(state_id):
    """Retrieves a State object: GET /api/v1/states/<state_id>"""
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    return jsonify(state.to_dict())


@app_views.route('/states/<state_id>', strict_slashes=False,
                 methods=['DELETE'])
def del_state(state_id):
    """Deletes a State object:: DELETE /api/v1/states/<state_id>"""
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    state.delete()
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/states', strict_slashes=False, methods=['POST'])
def post_state():
    """Creates a State: POST /api/v1/states"""
    new_state = request.get_json()
    if not new_state:
        abort(400, "Not a JSON")
    if "name" not in new_state:
        abort(400, "Missing name")
    state = State(**new_state)
    storage.new(state)
    storage.save()
    return make_response(jsonify(state.to_dict()), 201)


@app_views.route('/states/<state_id>', strict_slashes=False,
                 methods=['PUT'])
def put_state(state_id):
    """Updates a State object: PUT /api/v1/states/<state_id>"""
    state = storage.get(State, state_id)
    if not state:
        abort(404)

    body_req = request.get_json()
    if not body_req:
        abort(400, "Not a JSON")

    for key, val in body_req.items():
        if key != 'id' and key != 'created_at' and key != 'updated_at':
            setattr(state, key, val)

    storage.save()
    return make_response(jsonify(state.to_dict()), 200)
