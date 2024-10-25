#!/usr/bin/python3

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from .base_model import BaseModel
from .user import User
from .place import Place
from .review import Review
from .amenity import Amenity

DATABASE_URI = 'sqlite:///hbnb.db'
engine = create_engine(DATABASE_URI)
Session = scoped_session(sessionmaker(bind=engine))

BaseModel.metadata.create_all(engine)

def get_session():
    return Session()

__all__ = ["BaseModel", "User", "Place", "Review", "Amenity", "get_session"]
