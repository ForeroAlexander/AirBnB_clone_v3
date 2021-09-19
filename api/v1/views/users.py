#!/usr/bin/python3
"""RestFul API actions users
"""

from models.user import User
from models import storage
from api.v1.views import app_views
from flask import abort, jsonify, make_response, request


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def get_users():
    """ Retrieves a list of users """
    users = storage.all(User).values()
    users_list = []
    for user in users:
        users_list.append(user.to_dict())
    return jsonify(users_list)


@app_views.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
def get_user_id(user_id):
    """ Retrieves an user by id """
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    return jsonify(user.to_dict())


@app_views.route('/users/<user_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_users(user_id):
    """ Deletes an user by id """
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    storage.delete(user)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/users/<user_id>', methods=['DELETE'],
                 strict_slashes=False)
def post_users():
    """ Create an user object """
    if not request.get_json():
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    if "email" not in request.get_json():
        return make_response(jsonify({'error': 'Missing email'}), 400)
    if "password" not in request.get_json():
        return make_response(jsonify({'error': 'Missing password'}), 400)
    data = request.get_json()
    instance = User(**data)
    instance.save()
    return make_response(jsonify(instance.to_dict()), 201)


@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
def put_users(user_id):
    """ Updates an user object by id """
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    if not request.get_json():
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    key_ignore = ['id', 'email', 'created_at', 'updated_at']
    data = request.get_json()
    for key, value in data.items():
        if key not in key_ignore:
            setattr(user, key, value)
    storage.save()
    return make_response(jsonify(user.to_dict()), 200)
