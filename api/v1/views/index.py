#!/usr/bin/python3
"""module for the status route definition"""
from api.v1.views import app_views
from flask import jsonify

@app_views.route('/status', strict_slashes=False)
def status():
    """returns status"""
    return jsonify({"status": "OK"})
