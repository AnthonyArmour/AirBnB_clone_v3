#!/usr/bin/python3
"""states module for app_views"""
from flask import Flask, request, abort
from models.state import State
from models import storage
from api.v1.views import app_views
from flask import jsonify
from console import HBNBCommand


@app_views.route('/states/<state_id>', methods=['PUT', 'GET', 'DELETE'])
@app_views.route('/states/', methods=['POST', 'GET'])
@app_views.route('/states', methods=['POST', 'GET'])
def state_route(state_id=None):
    """state_route method determines request responses"""
    if request.method == 'GET' and state_id is None:
        states_lst = []
        for item in storage.all(State).values():
            states_lst.append(item.to_dict())
        return jsonify(states_lst)
    elif request.method == 'GET' and state_id is not None:
        state_obj = storage.get(State, state_id)
        if state_obj is None:
            abort(404, description="Not found")
        return jsonify(state_obj.to_dict())
    elif request.method == 'POST' and state_id == None:
        request_dict = request.get_json(silent=True)
        if request_dict is None:
            return jsonify({"error": "Not a JSON"}), 400
        else:
            if "name" in request_dict.keys():
                state_obj = State(**request_dict)
                state_obj.save()
                return jsonify(state_obj.to_dict()), 201
            else:
                return jsonify({"error": "Missing name"}), 400
    elif request.method == 'PUT' and state_id is not None:
        request_dict = request.get_json(silent=True)
        update_dict = {}
        for k, v in request_dict.items():
            if k != "id" and k != "updated_at" and k != "created_at":
                update_dict[k] = v
        if request_dict is None:
            return jsonify({"error": "Not a JSON"}), 400
        else:
            state_obj = storage.get(State, state_id)
            if state_obj is None:
                abort(404)
            else:
                for k, v in request_dict.items():
                    if k != "id" and k != "updated_at" and k != "created_at":
                        HBNBCommand().onecmd('update State {} {} "{}"'
                                             .format(state_id, k, v))
                storage.save()
                return jsonify(storage.get(State, state_id).to_dict()), 200
    elif request.method == 'DELETE' and state_id is not None:
        state_obj = storage.get(State, state_id)
        if state_obj is None:
            abort(404)
        storage.delete(state_obj)
        storage.save()
        return jsonify({}), 200
