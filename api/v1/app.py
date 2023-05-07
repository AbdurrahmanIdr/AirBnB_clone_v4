#!/usr/bin/python3
"""
starts a Flask web application
"""

from flask import Flask, jsonify
from models import storage
from api.v1.views import app_views
from os import getenv


app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown_db(exception):
    """closes the storage on teardown"""
    storage.close()


@app.errorhandler(404)
def invalid_route(e):
    return jsonify(error="Not found"), 404


if __name__ == "__main__":
    HBNB_API_HOST = getenv('HBNB_API_HOST')
    HBNB_API_PORT = getenv('HBNB_API_PORT')
    if HBNB_API_PORT and HBNB_API_HOST:
        app.run(host=HBNB_API_HOST, port=HBNB_API_PORT, threaded=True)
    else:
        app.run(host="0.0.0.0", port="5050", threaded=True)
