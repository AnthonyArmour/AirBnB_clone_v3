#!/usr/bin/python3
"""states module for app_views"""
from flask import Flask, request, abort
from models.state import State
from models.city import City
from models.place import Place
from models.review import Review
from models import storage
from api.v1.views import app_views
from flask import jsonify
from console import HBNBCommand


@app_views.route('/places/<place_id>/reviews', methods=['POST', 'GET'],
                 strict_slashes=False)
@app_views.route('/reviews/<review_id>', methods=['GET', 'DELETE', 'PUT'],
                 strict_slashes=False)
def places_reviews_route(review_id=None, place_id=None):
    """places_reviews_route method determines request responses"""
    if request.method == 'GET' and review_id is not None:
        review_obj = storage.get(Review, review_id)
        if review_obj is None:
            abort(404)
        return jsonify(review_obj.to_dict())
    elif request.method == 'GET' and place_id is not None:
        place_obj = storage.get(Place, place_id)
        if place_obj is None:
            abort(404)
        review_list = []
        for obj in storage.all(Review).values():
            if obj.place_id == place_id:
                review_list.append(obj.to_dict())
        return jsonify(review_list)
    elif request.method == 'DELETE' and review_id is not None:
        review_obj = storage.get(Review, review_id)
        if review_obj is None:
            abort(404)
        storage.delete(review_obj)
        storage.save()
        return jsonify({}), 200
    elif request.method == 'POST' and place_id is not None:
        place_obj = storage.get(Place, place_id)
        if place_obj is None:
            abort(404)
        request_dict = request.get_json(silent=True)
        if request_dict is None:
            return jsonify({"error": "Not a JSON"}), 400
        else:
            if "user_id" not in request_dict.keys():
                return jsonify({"error": "Missing user_id"}), 400
            elif "text" not in request_dict.keys():
                return jsonify({"error": "Missing text"}), 400
            elif storage.get(User, request_dict["user_id"]) is None:
                abort(404)
            else:
                request_dict["place_id"] = place_id
                review_obj = Review(**request_dict)
                review_obj.save()
                return jsonify(review_obj.to_dict()), 201
    elif request.method == 'PUT' and review_id is not None:
        request_dict = request.get_json(silent=True)
        if request_dict is None:
            return jsonify({"error": "Not a JSON"}), 400
        else:
            review_obj = storage.get(Review, review_id)
            if review_obj is None:
                abort(404)
            else:
                for k, v in request_dict.items():
                    if (k != "id" and
                        k != "updated_at" and k != "user_id" and
                            k != "created_at" and k != "place_id"):
                        HBNBCommand().onecmd('update Review {} {} "{}"'
                                             .format(review_id, k, v))
                storage.save()
                return jsonify(storage.get(Review, review_id).to_dict()), 200
