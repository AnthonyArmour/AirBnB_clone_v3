#!/usr/bin/python3
"""module for the status route definition"""
from api.v1.views import app_views
from flask import jsonify
from models import storage
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.user import User
from models.review import Review


@app_views.route('/status', strict_slashes=False)
def status():
    """returns status"""
    return jsonify({"status": "OK"})


@app_views.route('/stats', strict_slashes=False)
def stats():
    """returns count of all the classes"""
    stats_cnt = {
        'states': storage.count(State),
        'cities': storage.count(City),
        'amenities': storage.count(Amenity),
        'places': storage.count(Place),
        'reviews': storage.count(Review),
        'users': storage.count(User)
    }
    return jsonify(stats_cnt)
