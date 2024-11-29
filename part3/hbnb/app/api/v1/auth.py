# app/api/v1/auth.py

from flask import request
from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import create_access_token
from app.models.user import User
from app import bcrypt, db

api = Namespace('auth', description='Authentication operations')

login_model = api.model('Login', {
    'email': fields.String(required=True, description='User email'),
    'password': fields.String(required=True, description='User password')
})

@api.route('/login')
class Login(Resource):
    @api.expect(login_model)
    def post(self):
        """Authenticate user and return a JWT token"""
        credentials = api.payload
        
        user = User.query.filter_by(email=credentials['email']).first()
        
        if not user or not bcrypt.check_password_hash(user.password, credentials['password']):
            return {'error': 'Invalid credentials'}, 401

        access_token = create_access_token(identity={'id': user.id, 'is_admin': user.is_admin})
        
        return {'access_token': access_token}, 200
