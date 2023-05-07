#!/usr/bin/python3
"""
restapi for state object
"""

from flask import Flask, jsonify, abort, request
from models.state import State
from models import storage
from api.v1.views import app_views


@app_views.route("/states", methods=['GET'])
def fetch_states():
    allstate = storage.all(State)
    list_state = []
    for key in allstate:
        state = allstate[key]
        list_state.append(state.to_dict())
    return list_state


@app_views.route("/states/<state_id>", methods=['GET'])
def fetch_state(state_id):
    key_id = "State.{}".format(state_id)
    allstate = storage.all(State)
    if key_id in allstate.keys():
        state = allstate[key_id]
        return state.to_dict()
    abort(404)


@app_views.route("/states/<state_id>", methods=['DELETE'])
def del_state(state_id):
    allstates = storage.all(State)
    key = "State.{}".format(state_id)
    if key in allstates:
        allstates[key].delete()
        return {}
    abort(404)


@app_views.route("/states", methods=['POST'])
def add_state():
    new_dict = request.get_json()
    if not new_dict:
        return "Not a JSON", 400
    if "name" not in new_dict.keys():
        return "Missing name", 400
    new_state = State(**new_dict)
    storage.new(new_state)
    storage.save()
    new_state.save()
    return jsonify(new_state.to_dict()), 201


@app_views.route("/states/<state_id>", methods=['PUT'])
def edit_state(state_id):
    allstate = storage.all(State)
    key = "State.{}".format(state_id)
    if key not in allstate.keys():
        abort(404)
    new_data = request.get_json()
    if not new_data:
        return "Not a JSON", 400
    if "id" in new_data:
        del new_data["id"]
    if "updated_at" in new_data:
        del new_data["updated_at"]
    if "created_at" in new_data:
        del new_data["created_at"]
    state = allstate[key]
    state.__dict__.update(new_data)
    state.save()
    return jsonify(state.to_dict()), 200
