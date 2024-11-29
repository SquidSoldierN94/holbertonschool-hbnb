#!/usr/bin/python3

from sqlalchemy import Column, String, Float
from sqlalchemy.orm import relationship
from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db

api = Namespace('places', description='Place operations')

# Amenity Model
amenity_model = api.model('PlaceAmenity', {
    'id': fields.String(description='Amenity ID'),
    'name': fields.String(description='Name of the amenity')
})

# User Model
user_model = api.model('PlaceUser', {
    'id': fields.String(description='User ID'),
    'first_name': fields.String(description='First name of the owner'),
    'last_name': fields.String(description='Last name of the owner'),
    'email': fields.String(description='Email of the owner')
})

# Review Model
review_model = api.model('PlaceReview', {
    'id': fields.String(description='Review ID'),
    'text': fields.String(description='Text of the review'),
    'rating': fields.Integer(description='Rating of the place (1-5)'),
    'user_id': fields.String(description='ID of the user')
})

# Place Model
class Place(db.Model):
    __tablename__ = 'places'

    id = db.Column(db.String(60), primary_key=True)
    title = db.Column(db.String(128), nullable=False)
    description = db.Column(db.Text, nullable=True)
    price = db.Column(db.Float, nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    owner_id = db.Column(db.String(60), db.ForeignKey('users.id'), nullable=False)

    owner = db.relationship('User', backref='places', lazy=True)
    amenities = db.relationship('Amenity', backref='place', lazy=True)
    reviews = db.relationship('Review', backref='place', lazy=True)

# Place Model Serializer
place_model = api.model('Place', {
    'title': fields.String(required=True, description='Title of the place'),
    'description': fields.String(description='Description of the place'),
    'price': fields.Float(required=True, description='Price per night'),
    'latitude': fields.Float(required=True, description='Latitude of the place'),
    'longitude': fields.Float(required=True, description='Longitude of the place'),
    'owner_id': fields.String(required=True, description='ID of the owner'),
    'owner': fields.Nested(user_model, description='Owner details'),
    'amenities': fields.List(fields.Nested(amenity_model), required=True, description="List of amenities"),
    'reviews': fields.List(fields.Nested(review_model), description='List of reviews')
})

@api.route('/')
class PlaceList(Resource):
    @api.expect(place_model, validate=True)
    @api.response(201, 'Place successfully created')
    @api.response(400, 'Invalid input data')
    @jwt_required()
    def post(self):
        """Register a new place"""
        from app.services.facade import HBnBFacade
        facade = HBnBFacade()

        place_data = api.payload
        current_user = get_jwt_identity()
        place_data['owner_id'] = current_user

        try:
            new_place = facade.create_place(place_data)
            if not new_place:
                return {'error': 'Failed to create place'}, 400
            return {'id': new_place.id, 'title': new_place.title, 'description': new_place.description,
                    'price': new_place.price, 'latitude': new_place.latitude, 'longitude': new_place.longitude,
                    'owner_id': new_place.owner_id}, 201
        except ValueError as e:
            return {'error': str(e)}, 400

    @api.response(200, 'List of places retrieved successfully')
    def get(self):
        """Retrieve a list of all places"""
        from app.services.facade import HBnBFacade
        facade = HBnBFacade()

        places = facade.get_all_places()
        return [{'id': place.id, 'title': place.title, 'latitude': place.latitude,
                 'longitude': place.longitude} for place in places], 200

@api.route('/<place_id>')
class PlaceResource(Resource):
    @api.response(200, 'Place details retrieved successfully')
    @api.response(404, 'Place not found')
    def get(self, place_id):
        """Get place details by ID"""
        from app.services.facade import HBnBFacade
        facade = HBnBFacade()

        place = facade.get_place(place_id)
        if not place:
            return {'error': 'Place not found'}, 404
        return {
            'id': place.id,
            'title': place.title,
            'description': place.description,
            'price': place.price,
            'latitude': place.latitude,
            'longitude': place.longitude,
            'owner': {
                'id': place.owner.id,
                'first_name': place.owner.first_name,
                'last_name': place.owner.last_name,
                'email': place.owner.email
            },
            'amenities': [{'id': amenity.id, 'name': amenity.name} for amenity in place.amenities],
            'reviews': [{'id': review.id, 'text': review.text, 'rating': review.rating, 'user_id': review.user_id} for review in place.reviews]
        }, 200

    @api.expect(place_model, validate=True)
    @api.response(200, 'Place updated successfully')
    @api.response(404, 'Place not found')
    @api.response(400, 'Invalid input data')
    @jwt_required()
    def put(self, place_id):
        """Update a place's information"""
        from app.services.facade import HBnBFacade
        facade = HBnBFacade()

        place_data = api.payload
        current_user = get_jwt_identity()
        place = facade.get_place(place_id)

        if place.owner_id != current_user:
            return {'error': 'Unauthorized action'}, 403

        try:
            updated_place = facade.update_place(place_id, place_data, current_user)
            if not updated_place:
                return {'error': 'Place not found'}, 404
            return {'message': 'Place updated successfully'}, 200
        except ValueError as e:
            return {'error': str(e)}, 400
