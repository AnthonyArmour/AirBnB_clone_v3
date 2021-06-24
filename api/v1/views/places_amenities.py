#!/usr/bin/python3
"""module for places_amenities view"""
from flask import Flask, abort, request
from models.city import City
from models.place import Place
from models.user import User
from models.amenity import Amenity
from models import storage
from api.v1.views import app_views
from flask import jsonify
from console import HBNBCommand
import os


@app_views.route('/places/<place_id>/amenities', methods=['GET'],
                 strict_slashes=False)
@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 methods=['DELETE', 'POST'], strict_slashes=False)
def db_route(place_id=None, amenity_id=None):
    """route method to determin request respon DBStorage"""
    if os.getenv("HBNB_TYPE_STORAGE") != "db":
        fs_route(place_id, amenity_id)
        return
    from models.place import place_amenity
    if request.method == 'GET' and place_id is not None:
        place_obj = storage.get(Place, place_id)
        if place_obj is None:
            abort(404)
        amen_id_lst = []
        for obj in storage.all(place_amenity).values():
            if obj[0] == place_id:
                amen_id_lst.append(obj[1])
        amen_obj_lst = []
        for id in amen_id_lst:
            amen_obj_lst.append(storage.get(Amenity, id).to_dict())
        return jsonify(amen_obj_lst)
    elif (request.method == 'DELETE' and place_id is not None and
            amenity_id is not None):
        place_obj = storage.get(Place, place_id)
        amenity_obj = storage.get(Amenity, amenity_id)
        if place_obj is None or amenity_obj is None:
            abort(404)
        for obj in storage.all(place_amenity).values():
            if obj[0] == place_id and obj[1] == amenity_id:
                storage.delete(amenity_obj)
                storage.save()
                return jsonify({}), 200
        abort(404)
    elif (request.method == 'POST' and place_id is not None and
          amenity_id is not None):
        place_obj = storage.get(Place, place_id)
        amenity_obj = storage.get(Amenity, amenity_id)
        if place_obj is None or amenity_obj is None:
            abort(404)
        for obj in storage.all(place_amenity).values():
            if obj[0] == place_id and obj[1] == amenity_id:
                return jsonify(storage.get(Amenity, amenity_id).to_dict()), 200
        place_obj.amenities.append(amenity_obj)
        storage.save()
        return jsonify(storage.get(Amenity, amenity_id).to_dict()), 200


def fs_route(place_id, amenity_id):
    """routh method to determine request respon FileStorage"""
    if request.method == 'GET' and place_id is not None:
        place_obj = storage.get(Place, place_id)
        if place_obj is None:
            abort(404)
        amen_obj_lst = []
        for id in place_obj.amenity_ids:
            amen_obj_lst.append(storage.get(Amenity, id).to_dict())
        return jsonify(amen_obj_lst)
    elif (request.method == 'DELETE' and place_id is not None and
            amenity_id is not None):
        place_obj = storage.get(Place, place_id)
        amenity_obj = storage.get(Amenity, amenity_id)
        if place_obj is None or amenity_obj is None:
            abort(404)
        if amenity_id in place_obj.amenity_ids:
            storage.delete(amenity_obj)
            storage.save()
            return jsonify({}), 200
        abort(404)
    elif (request.method == 'POST' and place_id is not None and
            amenity_id is not None):
        place_obj = storage.get(Place, place_id)
        amenity_obj = storage.get(Amenity, amenity_id)
        if place_obj is None or amenity_obj is None:
            abort(404)
        for id in place_obj.amenity_ids:
            if id == amenity_id:
                return jsonify(storage.get(Amenity, amenity_id).to_dict()), 200
        place_obj.amenity_ids.append(amenity_id)
        storage.save()
        return jsonify(storage.get(Amenity, amenity_id).to_dict()), 200
