#!/usr/bin/python3
"""states module for app_views"""
from flask import Flask, request, abort
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.users import User
from models import storage
from api.v1.views import app_views
from flask import jsonify
from console import HBNBCommand


@app_views.route('/users', methods=['POST', 'GET'],
                 strict_slashes=False)
@app_views.route('/users/<user_id>', methods=['GET', 'DELETE', 'PUT'],
                 strict_slashes=False)
def user_route(user_id=None):
    """amenity_route method determines request responses"""
    if request.method == 'GET' and user_id is None:
        user_lst = storage.all(Amenity).values()
        new_user_list = []
        for obj in user_lst:
            new_user_list.append(obj.to_dict())
        return jsonify(new_user_list)
    elif request.method == 'GET' and user_id is not None:
        user_obj = storage.get(User, user_id)
        if user_obj is None:
            abort(404, description="Not found")
        return jsonify(user_obj.to_dict())
    elif request.method == 'POST' and user_id is None:
        request_dict = request.get_json(silent=True)
        if request_dict is None:
            return jsonify({"error": "Not a JSON"}), 400
        else:
            if "email" not in request_dict.keys():
                return jsonify({"error": "Missing email"}), 400
            elif "password" not in request_dict.keys():
                return jsonify({"error": "Missing password"}), 400
            else:
                user_obj = User(**request_dict)
                user_obj.save()
                return jsonify(user_obj.to_dict()), 201
    elif request.method == 'PUT' and user_id is not None:
        request_dict = request.get_json(silent=True)
        if request_dict is None:
            return jsonify({"error": "Not a JSON"}), 400
        else:
            user_obj = storage.get(User, user_id)
            if user_obj is None:
                abort(404)
            else:
                for k, v in request_dict.items():
                    if (k != "id" and k != "updated_at" and
                        k != "created_at" and k != "email"):
                        HBNBCommand().onecmd('update User {} {} "{}"'
                                             .format(user_id, k, v))
                storage.save()
                return jsonify(storage.get(User, user_id).to_dict()), 200
    elif request.method == 'DELETE' and user_id is not None:
        user_obj = storage.get(User, user_id)
        if user_obj is None:
            abort(404)
        storage.delete(user_obj)
        storage.save()
        return jsonify({}), 200
