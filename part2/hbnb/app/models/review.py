#!/usr/bin/python3

from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship
from .base_model import BaseModel

class Review(BaseModel):
    """Review model definition"""
    
    __tablename__ = 'reviews'
    
    id = Column(String(60), primary_key=True)
    text = Column(String, nullable=False)
    rating = Column(Integer, nullable=False)
    user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
    place_id = Column(String(60), ForeignKey('places.id'), nullable=False)

    user = relationship('User', backref='reviews')
    place = relationship('Place', backref='reviews')
