#!/usr/bin/python3
"""states module for app_views"""
from flask import Flask, request, abort
from models.state import State
from models.city import City
from models import storage
from api.v1.views import app_views
from flask import jsonify
from console import HBNBCommand


@app_views.route('/states/<state_id>/cities', methods=['POST', 'GET'],
                 strict_slashes=False)
@app_views.route('/cities/<city_id>', methods=['GET', 'DELETE', 'PUT'],
                 strict_slashes=False)
def city_route(state_id=None, city_id=None):
    """state_route method determines request responses"""
    if request.method == 'GET' and city_id is not None:
        city_obj = storage.get(City, city_id)
        if city_obj is None:
            abort(404)
        return jsonify(city_obj.to_dict())
    elif request.method == 'GET' and state_id is not None:
        state_obj = storage.get(State, state_id)
        if state_obj is None:
            abort(404, description="Not found")
        final_city_lst = []
        city_list = storage.all(City).values()
        for obj in city_list:
            if obj.state_id == state_id:
                final_city_lst.append(obj.to_dict())
        return jsonify(final_city_lst)
    elif request.method == 'POST' and state_id is not None:
        state_obj = storage.get(State, state_id)
        if state_obj is None:
            abort(404)
        request_dict = request.get_json(silent=True)
        if request_dict is None:
            return jsonify({"error": "Not a JSON"}), 400
        else:
            if "name" in request_dict.keys():
                request_dict["state_id"] = state_id
                city_obj = City(**request_dict)
                city_obj.save()
                return jsonify(city_obj.to_dict()), 201
            else:
                return jsonify({"error": "Missing name"}), 400
    elif request.method == 'PUT' and city_id is not None:
        request_dict = request.get_json(silent=True)
        if request_dict is None:
            return jsonify({"error": "Not a JSON"}), 400
        else:
            city_obj = storage.get(City, city_id)
            if city_obj is None:
                abort(404)
            else:
                for k, v in request_dict.items():
                    if (k != "id" and
                        k != "updated_at" and
                            k != "created_at" and k != "state_id"):
                        HBNBCommand().onecmd('update City {} {} "{}"'
                                             .format(city_id, k, v))
                storage.save()
                return jsonify(storage.get(City, city_id).to_dict()), 200
    elif request.method == 'DELETE' and city_id is not None:
        city_obj = storage.get(City, city_id)
        if city_obj is None:
            abort(404)
        storage.delete(city_obj)
        storage.save()
        return jsonify({}), 200
