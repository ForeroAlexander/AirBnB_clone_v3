#!/usr/bin/python3
"""RestFul API actions amenities
"""

from models.place import Place
from models.amenity import Amenity
from models import storage
from api.v1.views import app_views
from os import environ
from flask import abort, jsonify, make_response, request


@app_views.route('places/<place_id>/amenities', methods=['GET'],
                 strict_slashes=False)
def get_places_amenities(place_id):
    """ Retrieves amenities of a place """
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    if environ.get("HBNB_TYPE_STORAGE") == 'db':
        amenities = [amenity.to_dict() for amenity in place.amenities]
    else:
        amenities = [storage.get(Amenity, amenity_id).to_dict()
                     for amenity_id in place.amenity_ids]
    return jsonify(amenities)


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_places_amenities(place_id, amenity_id):
    """ Deletes an specific amenity of a place by id """
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    if environ.get("HBNB_TYPE_STORAGE") == 'db':
        if amenity not in place.amenities:
            abort(404)
        place.amenities.remove(amenity)
    else:
        if amenity_id not in place.amenity_ids:
            abort(404)
        place.amenities.remove(amenity)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/places/<place_id>/amenities/<amenity_id>', methods=['POST'],
                 strict_slashes=False)
def post_places_amenities(place_id, amenity_id):
    """ Links an amenity object with a place """
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    if environ.get("HBNB_TYPE_STORAGE") == 'db':
        if amenity in place.amenities:
            return make_response(jsonify(amenity.to_dict()), 200)
        else:
            place.amenities.append(amenity)
    else:
        if amenity_id in place.amenity_ids:
            return make_response(jsonify(amenity.to_dict()), 200)
        else:
            place.amenity_ids.append(amenity_id)
    storage.save()
    return make_response(jsonify(amenity.to_dict()), 201)