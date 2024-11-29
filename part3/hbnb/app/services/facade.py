from app.models import Place, Review, User, Amenity
from app import db
from sqlalchemy.exc import IntegrityError

class HBnBFacade:
    def __init__(self):
        pass

    # Create a new place
    def create_place(self, place_data):
        """Create a new place"""
        try:
            new_place = Place(
                id=place_data['id'],
                title=place_data['title'],
                description=place_data.get('description'),
                price=place_data['price'],
                latitude=place_data['latitude'],
                longitude=place_data['longitude'],
                owner_id=place_data['owner_id']
            )

            # Add amenities to the place if provided
            if 'amenities' in place_data:
                amenities = place_data['amenities']
                new_place.amenities = [Amenity(id=amenity['id'], name=amenity['name']) for amenity in amenities]
            
            db.session.add(new_place)
            db.session.commit()
            return new_place
        except IntegrityError:
            db.session.rollback()
            raise ValueError("Place could not be created due to integrity constraints.")
        except Exception as e:
            db.session.rollback()
            raise ValueError(f"An error occurred while creating the place: {str(e)}")

    # Get a single place by ID
    def get_place(self, place_id):
        """Get a place by ID"""
        place = Place.query.filter_by(id=place_id).first()
        if not place:
            raise ValueError("Place not found")
        return place

    # Get all places
    def get_all_places(self):
        """Get all places"""
        return Place.query.all()

    # Update a place
    def update_place(self, place_id, place_data, current_user):
        """Update a place's details"""
        place = self.get_place(place_id)
        
        if place.owner_id != current_user:
            raise PermissionError("You do not have permission to update this place.")
        
        try:
            place.title = place_data['title']
            place.description = place_data.get('description', place.description)
            place.price = place_data['price']
            place.latitude = place_data['latitude']
            place.longitude = place_data['longitude']

            # Update amenities
            if 'amenities' in place_data:
                place.amenities = [Amenity(id=amenity['id'], name=amenity['name']) for amenity in place_data['amenities']]
            
            db.session.commit()
            return place
        except Exception as e:
            db.session.rollback()
            raise ValueError(f"An error occurred while updating the place: {str(e)}")

    # Create a new review for a place
    def create_review(self, review_data):
        """Create a review for a place"""
        try:
            review = Review(
                text=review_data['text'],
                rating=review_data['rating'],
                user_id=review_data['user_id'],
                place_id=review_data['place_id']
            )
            review.validate()  # Validation for rating between 1 and 5
            db.session.add(review)
            db.session.commit()
            return review
        except ValueError as e:
            db.session.rollback()
            raise ValueError(f"Invalid review data: {str(e)}")
        except Exception as e:
            db.session.rollback()
            raise ValueError(f"An error occurred while creating the review: {str(e)}")

    # Get a review by ID
    def get_review(self, review_id):
        """Get a review by ID"""
        review = Review.query.filter_by(id=review_id).first()
        if not review:
            raise ValueError("Review not found")
        return review

    # Get all reviews
    def get_all_reviews(self):
        """Get all reviews"""
        return Review.query.all()

    # Get all reviews for a specific place
    def get_reviews_for_place(self, place_id):
        """Get all reviews for a specific place"""
        place = self.get_place(place_id)
        return place.reviews

    # Delete a review by ID
    def delete_review(self, review_id, current_user):
        """Delete a review by ID if the user is the owner or reviewer"""
        review = self.get_review(review_id)
        
        if review.user_id != current_user:
            raise PermissionError("You do not have permission to delete this review.")
        
        try:
            db.session.delete(review)
            db.session.commit()
            return {"message": "Review successfully deleted."}
        except Exception as e:
            db.session.rollback()
            raise ValueError(f"An error occurred while deleting the review: {str(e)}")

    # Delete a place by ID
    def delete_place(self, place_id, current_user):
        """Delete a place by ID if the user is the owner"""
        place = self.get_place(place_id)
        
        if place.owner_id != current_user:
            raise PermissionError("You do not have permission to delete this place.")
        
        try:
            db.session.delete(place)
            db.session.commit()
            return {"message": "Place successfully deleted."}
        except Exception as e:
            db.session.rollback()
            raise ValueError(f"An error occurred while deleting the place: {str(e)}")
