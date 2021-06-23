#!/usr/bin/python3
"""module that contains methods for an API"""
from models import storage
from flask import Flask, Blueprint
from api.v1.views import app_views
import os


app = Flask(__name__)
app.register_blueprint(app_views, url_prefix='/api/v1')
HOST = os.getenv("HBNB_API_HOST")
PORT = os.getenv("HBNB_API_PORT") 


@app.teardown_appcontext
def tear_down(exception):
    """closes app"""
    if storage:
        storage.close()


if __name__ == "__main__":
    if HOST is None:
        HOST = "0.0.0.0"
    if PORT is None:
        PORT = 5000
    app.run(host=HOST, port=PORT, threaded=True)
