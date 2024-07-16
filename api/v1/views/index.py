#!/usr/bin/python3
"""Index"""
from api.v1.views import app_views
from flask import jsonify
from models import storage


@app_views.route('/status', strict_slashes=False, methods=['GET'])
def status():
    """Returns JSON status 'OK'"""
    return jsonify(status="OK")


@app_views.route('/stats', methods=['GET'])
def stats():
    """Returns JSON count of each instance type"""
    return jsonify(amenities=storage.count("Amenity") if storage.count("Amenity") is not None else 0,
                   cities=storage.count("City") if storage.count("City") is not None else 0,
                   places=storage.count("Place") if storage.count("Place") is not None else 0,
                   reviews=storage.count("Review") if storage.count("Review") is not None else 0,
                   states=storage.count("State") if storage.count("State") is not None else 0,
                   users=storage.count("User") if storage.count("User") is not None else 0)
