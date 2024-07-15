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
