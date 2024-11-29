# app/models/user.py

from sqlalchemy import Column, String, Boolean
from .base_model import BaseModel
from app import bcrypt

class User(BaseModel):
    __tablename__ = 'users'

    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    email = Column(String(100), nullable=False, unique=True)
    password = Column(String(128), nullable=False)
    is_admin = Column(Boolean, default=False)

    def __init__(self, first_name, last_name, email, password=None, is_admin=False):
        super().__init__()
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.is_admin = is_admin
        if password:
            self.password = bcrypt.generate_password_hash(password).decode('utf-8')
        self.validate()

    def verify_password(self, password):
        """Verifies if the provided password matches the hashed password."""
        return bcrypt.check_password_hash(self.password, password)

    def validate(self):
        if not self.first_name or not self.last_name:
            raise ValueError("First name and last name cannot be empty")
        if not self.email or "@" not in self.email:
            raise ValueError("Invalid email format")
