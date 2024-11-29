#!/usr/bin/python3

from flask import request, jsonify
from flask_restx import Namespace, Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from models.user import User

api = Namespace('users', description='User related operations')

@api.route('/')
class UserList(Resource):
    @jwt_required()
    def get(self):
        """Get all users (Protected)"""
        users = User.query.all()
        result = []
        for user in users:
            user_data = {
                'id': user.id,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'email': user.email
            }
            result.append(user_data)
        return jsonify(result)

    def post(self):
        """Create a new user"""
        data = request.get_json()
        if not data or 'password' not in data:
            return {"message": "Password is required"}, 400

        new_user = User(
            first_name=data.get('first_name'),
            last_name=data.get('last_name'),
            email=data.get('email'),
            password=data.get('password')
        )

        db.session.add(new_user)
        db.session.commit()

        return {"id": new_user.id, "message": "User created successfully"}, 201

@api.route('/<int:user_id>')
class UserDetail(Resource):
    @jwt_required()
    def get(self, user_id):
        """Get a user by ID (Protected)"""
        user = User.query.get_or_404(user_id)
        user_data = {
            'id': user.id,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email,
        }
        return user_data

    @jwt_required()
    def delete(self, user_id):
        """Delete a user by ID (Protected)"""
        user = User.query.get_or_404(user_id)
        db.session.delete(user)
        db.session.commit()
        return {"message": "User deleted successfully"}, 200
