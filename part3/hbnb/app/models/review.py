#!/usr/bin/python3

from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship
from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db

api = Namespace('reviews', description='Review operations')

# Review Model Serializer
review_model = api.model('Review', {
    'text': fields.String(required=True, description='Text of the review'),
    'rating': fields.Integer(required=True, description='Rating of the place (1-5)'),
    'place_id': fields.String(required=True, description='ID of the place')
})

# Review Model
class Review(db.Model):
    __tablename__ = 'reviews'
    
    id = Column(String(60), primary_key=True)
    text = Column(String, nullable=False)
    rating = Column(Integer, nullable=False)
    user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
    place_id = Column(String(60), ForeignKey('places.id'), nullable=False)

    user = relationship('User', backref='reviews')
    place = relationship('Place', backref='reviews')

    def validate(self):
        """Ensure that the rating is between 1 and 5"""
        if not (1 <= self.rating <= 5):
            raise ValueError("Rating must be between 1 and 5.")

@api.route('/')
class ReviewList(Resource):
    @api.expect(review_model, validate=True)
    @api.response(201, 'Review successfully created')
    @api.response(400, 'Invalid input data')
    @jwt_required()
    def post(self):
        """Create a new review"""
        from app.services.facade import HBnBFacade
        facade = HBnBFacade()

        review_data = api.payload
        current_user = get_jwt_identity()
        review_data['user_id'] = current_user

        try:
            new_review = facade.create_review(review_data)
            if not new_review:
                return {'error': 'Failed to create review'}, 400
            return {'id': new_review.id, 'text': new_review.text, 'rating': new_review.rating,
                    'user_id': new_review.user_id, 'place_id': new_review.place_id}, 201
        except ValueError as e:
            return {'error': str(e)}, 400

    @api.response(200, 'List of reviews retrieved successfully')
    def get(self):
        """Retrieve a list of all reviews"""
        from app.services.facade import HBnBFacade
        facade = HBnBFacade()

        reviews = facade.get_all_reviews()
        return [{'id': review.id, 'text': review.text, 'rating': review.rating,
                 'user_id': review.user_id, 'place_id': review.place_id} for review in reviews], 200

@api.route('/<review_id>')
class ReviewResource(Resource):
    @api.response(200, 'Review details retrieved successfully')
    @api.response(404, 'Review not found')
    def get(self, review_id):
        """Get review details by ID"""
        from app.services.facade import HBnBFacade
        facade = HBnBFacade()

        review = facade.get_review(review_id)
        if not review:
            return {'error': 'Review not found'}, 404
        return {
            'id': review.id,
            'text': review.text,
            'rating': review.rating,
            'user_id': review.user_id,
            'place_id': review.place_id
        }, 200
