#!/usr/bin/python3

from sqlalchemy import Column, String
from .base_model import BaseModel

class User(BaseModel):
    __tablename__ = 'users'

    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    email = Column(String(100), nullable=False)

    def __init__(self, first_name, last_name, email):
        super().__init__()
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.validate()

    def validate(self):
        if not self.first_name or not self.last_name:
            raise ValueError("First name and last name cannot be empty")
        if not self.email or "@" not in self.email:
            raise ValueError("Invalid email format")
