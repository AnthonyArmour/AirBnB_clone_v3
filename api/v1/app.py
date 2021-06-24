#!/usr/bin/python3
"""module that contains methods for an API"""
from models import storage
from flask import Flask, Blueprint, jsonify
from api.v1.views import app_views
import os
from flask_cors import CORS


app = Flask(__name__)
app.register_blueprint(app_views, url_prefix='/api/v1')
cors = CORS(app, resources={"/*": {"origins": "0.0.0.0"}})
HOST = os.getenv("HBNB_API_HOST")
PORT = os.getenv("HBNB_API_PORT")


@app.teardown_appcontext
def tear_down(exception):
    """closes app"""
    if storage:
        storage.close()


@app.errorhandler(404)
def not_found(e):
    """JSON ERROR message"""
    return jsonify({"error": "Not found"}), 404


if __name__ == "__main__":
    if HOST is None:
        HOST = "0.0.0.0"
    if PORT is None:
        PORT = 5000
    app.run(host=HOST, port=PORT, threaded=True)
