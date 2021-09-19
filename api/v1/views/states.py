#!/usr/bin/python3
"""RestFul API actions State
"""

from api.v1.views import app_views
from flask import jsonify, request, abort, make_response
from models import storage
from models.state import State


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def states_all():
    """Retrieves the list of all State objects
    """
    states_obj = storage.all('State')
    list_states = []
    for obj in states_obj.values():
        list_states.append(obj.to_dict())
    return jsonify(list_states)


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def states_id(state_id=None):
    """Retrieve a states by Id
    """
    state = storage.get('State', state_id)
    if state:
        return jsonify(state.to_dict())
    abort(404)


@app_views.route('/states/<state_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_states(state_id=None):
    """Deletes a State object
    """
    state = storage.get(State, state_id)
    if state:
        storage.delete(state)
        storage.save()
        return make_response(jsonify({}), 200)
    return abort(404)


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def post_states(state_id=None):
    """Creates a State
    """
    dict_json = request.get_json()
    if not dict_json:
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    if 'name' not in dict_json:
        return make_response(jsonify({'error': 'Missing name'}), 400)
    new_state = State(**dict_json)
    storage.new(new_state)
    storage.save()
    return make_response(jsonify(new_state.to_dict()), 201)


@app_views.route('/states/<state_id>', methods=['PUT'],
                 strict_slashes=False)
def put_states(state_id=None):
    """ Updates a State object """
    dict_json = request.get_json()
    if not dict_json:
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    states_obj = storage.get('State', state_id)
    if states_obj:
        for key, value in dict_json.items():
            setattr(states_obj, key, value)
        storage.save()
        return make_response(jsonify(states_obj.to_dict()), 200)
    else:
        return abort(404)
