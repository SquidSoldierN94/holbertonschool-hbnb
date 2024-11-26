#!/usr/bin/python3

from sqlalchemy import Column, String
from .base_model import BaseModel

class Amenity(BaseModel):
    __tablename__ = 'amenities'

    name = Column(String(100), nullable=False)

    def __init__(self, name):
        super().__init__()
        self.name = name
        self.validate()

    def validate(self):
        if not self.name:
            raise ValueError("Amenity name cannot be empty")
