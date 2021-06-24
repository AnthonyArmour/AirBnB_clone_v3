#!/usr/bin/python3
"""places module for app_views"""
from flask import Flask, request, abort
from models.city import City
from models.place import Place
from models import storage
from api.v1.views import app_views
from flask import jsonify
from console import HBNBCommand


@app_views.route('/cities/<city_id>/places', methods=['POST', 'GET'],
                 strict_slashes=False)
@app_views.route('/places/<place_id>', methods=['GET', 'DELETE', 'PUT'],
                 strict_slashes=False)
def place_route(place_id=None, city_id=None):
    """place_route method determines request responses"""
    if request.method == 'GET' and place_id is not None:
        place_obj = storage.get(Place, place_id)
        if place_obj is None:
            abort(404)
        return jsonify(place_obj.to_dict())
    elif request.method == 'GET' and city_id is not None:
        city_obj = storage.get(City, city_id)
        if city_obj is None:
            abort(404, description="Not found")
        places_lst = []
        for obj in storage.all(Place).values():
            if obj.city_id == city_id:
                places_lst.append(obj.to_dict())
        return jsonify(places_lst)
    elif request.method == 'POST' and city_id is not None:
        city_obj = storage.get(City, city_id)
        if city_obj is None:
            abort(404)
        request_dict = request.get_json(silent=True)
        if request_dict is None:
            return jsonify({"error": "Not a JSON"}), 400
        else:
            if "name" not in request_dict.keys():
                return jsonify({"error": "Missing name"}), 400
            elif "user_id" not in request_dict.keys():
                return jsonify({"error": "Missing user_id"}), 400
            elif storage.get(User, request_dict["user_id"]) is None:
                abort(404)
            else:
                request_dict["city_id"] = city_id
                place_obj = Place(**request_dict)
                place_obj.save()
                return jsonify(place_obj.to_dict()), 201
    elif request.method == 'PUT' and place_id is not None:
        request_dict = request.get_json(silent=True)
        if request_dict is None:
            return jsonify({"error": "Not a JSON"}), 400
        else:
            place_obj = storage.get(Place, place_id)
            if place_obj is None:
                abort(404)
            else:
                for k, v in request_dict.items():
                    if (k != "id" and
                        k != "updated_at" and k != "user_id" and
                            k != "created_at" and k != "city_id"):
                        HBNBCommand().onecmd('update Place {} {} "{}"'
                                             .format(place_id, k, v))
                storage.save()
                return jsonify(storage.get(Place, place_id).to_dict()), 200
    elif request.method == 'DELETE' and place_id is not None:
        place_obj = storage.get(Place, place_id)
        if place_obj is None:
            abort(404)
        storage.delete(place_obj)
        storage.save()
        return jsonify({}), 200
