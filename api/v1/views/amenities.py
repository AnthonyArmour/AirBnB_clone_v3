#!/usr/bin/python3
"""states module for app_views"""
from flask import Flask, request, abort
from models.state import State
from models.city import City
from models.amenity import Amenity
from models import storage
from api.v1.views import app_views
from flask import jsonify
from console import HBNBCommand


@app_views.route('/amenities', methods=['POST', 'GET'],
                 strict_slashes=False)
@app_views.route('/amenities/<amenity_id>', methods=['GET', 'DELETE', 'PUT'],
                 strict_slashes=False)
def amenity_route(amenity_id=None):
    """amenity_route method determines request responses"""
    # retrieves list of all Amenity objects using GET
    if request.method == 'GET' and amenity_id is None:
        amenity_lst = storage.all(Amenity).values()
        new_amenity_list = []
        for obj in amenity_lst:
            new_amenity_list.append(obj.to_dict())
        return jsonify(new_amenity_list)
    # retrieves Amenity obj using GET
    # if amenit_id is not linked to obj then raise 404
    elif request.method == 'GET' and amenity_id is not None:
        amenity_obj = storage.get(Amenity, amenity_id)
        if amenity_obj is None:
            abort(404, description="Not found")
        return jsonify(amenity_obj.to_dict())
    # creates a new Amenity using POST
    # raises 400 if request body not a valid JSON
    # raises 400 if dict does not contain a name
    # on success returns 201 and new Amenity
    elif request.method == 'POST' and amenity_id is None:
        request_dict = request.get_json(silent=True)
        if request_dict is None:
            return jsonify({"error": "Not a JSON"}), 400
        else:
            if "name" in request_dict.keys():
                amenity_obj = Amenity(**request_dict)
                amenity_obj.save()
                return jsonify(amenity_obj.to_dict()), 201
            else:
                return jsonify({"error": "Missing name"}), 400
    # updates an Amenity obj using POST
    # if HTTP request body not valid JSON raise 400
    # if amenity_id is not linked to obj raise 404
    # Returns changed obj with code 200
    elif request.method == 'PUT' and amenity_id is not None:
        request_dict = request.get_json(silent=True)
        if request_dict is None:
            return jsonify({"error": "Not a JSON"}), 400
        else:
            amenity_obj = storage.get(Amenity, amenity_id)
            if amenity_obj is None:
                abort(404)
            else:
                for k, v in request_dict.items():
                    if k != "id" and k != "updated_at" and k != "created_at":
                        HBNBCommand().onecmd('update Amenity {} {} "{}"'
                                             .format(amenity_id, k, v))
                storage.save()
                return jsonify(storage.get(Amenity, amenity_id).to_dict()), 200
    # deletes and Amenity obj using DELETE
    # raises 404 if amenity_id not linked to obj
    # on success returns empty dict with code 200
    elif request.method == 'DELETE' and amenity_id is not None:
        amenity_obj = storage.get(Amenity, amenity_id)
        if amenity_obj is None:
            abort(404)
        storage.delete(amenity_obj)
        storage.save()
        return jsonify({}), 200
