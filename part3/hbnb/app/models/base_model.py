#!/usr/bin/python3

import uuid
from datetime import datetime
from sqlalchemy import Column, String, DateTime
from app import db  # Ensure this path is correct based on your project structure

class BaseModel(db.Model):
    __abstract__ = True

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def save(self):
        """Update the updated_at timestamp and commit the change."""
        self.updated_at = datetime.utcnow()
        db.session.add(self)
        db.session.commit()

    def update(self, data):
        """Update the model with the given data and commit the change."""
        for key, value in data.items():
            if hasattr(self, key):
                setattr(self, key, value)
        self.save()

    def to_dict(self):
        """Convert model attributes to dictionary."""
        return {
            'id': self.id,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
        }
