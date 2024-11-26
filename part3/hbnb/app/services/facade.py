#!/usr/bin/python3

from app import db
from app.models import Place, User, Review, Amenity

class HBnBFacade:
    def create_place(self, place_data):
        owner_id = place_data.get('owner_id')
        owner = User.query.get(owner_id)

        if not owner:
            raise ValueError("Owner ID does not exist.")

        new_place = Place(
            title=place_data['title'],
            description=place_data.get('description'),
            price=place_data['price'],
            latitude=place_data['latitude'],
            longitude=place_data['longitude'],
            owner=owner
        )
        
        amenities = place_data.get('amenities', [])
        for amenity in amenities:
            amenity_obj = Amenity.query.get(amenity['id'])
            if amenity_obj:
                new_place.amenities.append(amenity_obj)

        db.session.add(new_place)
        db.session.commit()
        return new_place

    def get_all_places(self):
        return Place.query.all()

    def get_place(self, place_id):
        return Place.query.get(place_id)

    def update_place(self, place_id, place_data):
        place = self.get_place(place_id)
        if not place:
            return None
        
        place.title = place_data.get('title', place.title)
        place.description = place_data.get('description', place.description)
        place.price = place_data.get('price', place.price)
        place.latitude = place_data.get('latitude', place.latitude)
        place.longitude = place_data.get('longitude', place.longitude)

        place.amenities.clear()
        amenities = place_data.get('amenities', [])
        for amenity in amenities:
            amenity_obj = Amenity.query.get(amenity['id'])
            if amenity_obj:
                place.amenities.append(amenity_obj)

        db.session.commit()
        return place

    def create_review(self, review_data):
        """Creates a new review."""
        new_review = Review(**review_data)  # Unpack review data into Review object
        db.session.add(new_review)
        db.session.commit()
        return new_review

    def get_all_reviews(self):
        """Returns all reviews."""
        return Review.query.all()

    def get_review(self, review_id):
        """Gets a review by its ID."""
        return Review.query.get(review_id)

    def update_review(self, review_id, review_data):
        """Updates a review's information."""
        review = self.get_review(review_id)
        if not review:
            return None

        review.text = review_data.get('text', review.text)
        review.rating = review_data.get('rating', review.rating)
        review.user_id = review_data.get('user_id', review.user_id)
        review.place_id = review_data.get('place_id', review.place_id)

        db.session.commit()
        return review

    def delete_review(self, review_id):
        """Deletes a review."""
        review = self.get_review(review_id)
        if not review:
            raise ValueError("Review not found.")
        
        db.session.delete(review)
        db.session.commit()

    def get_reviews_by_place(self, place_id):
        """Gets all reviews for a specific place."""
        return Review.query.filter_by(place_id=place_id).all()

    def get_user_by_email(self, email):
        """Gets a user by their email address."""
        return User.query.filter_by(email=email).first()
