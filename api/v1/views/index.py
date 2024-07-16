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
    return jsonify(amenities=storage.count("Amenity") or 0,
                   cities=storage.count("City") or 0,
                   places=storage.count("Place") or 0,
                   reviews=storage.count("Review") or 0,
                   states=storage.count("State") or 0,
                   users=storage.count("User") or 0)
