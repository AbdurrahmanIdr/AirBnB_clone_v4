#!/usr/bin/python3
"""
Restful Api
"""

from api.v1.views import app_views
from flask import jsonify
from models import storage


@app_views.route("/status")
def ret_status():
    return jsonify(status="OK")


@app_views.route("/stats")
def ret_stats():
    from models.amenity import Amenity
    from models.review import Review
    from models.user import User
    from models.place import Place
    from models.state import State
    from models.city import City
    return {"amenities": storage.count(Amenity),
            "cities": storage.count(City),
            "places": storage.count(Place),
            "reviews": storage.count(Review),
            "states": storage.count(State),
            "users": storage.count(User)
            }
