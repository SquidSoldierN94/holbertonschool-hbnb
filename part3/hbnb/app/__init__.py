# app/__init__.py

from flask import Flask
from flask_restx import Api
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
import os

db = SQLAlchemy()
bcrypt = Bcrypt()

def create_app(config_name=None):
    app = Flask(__name__)
    
    # Import the config dictionary
    from config import config
    
    # Set the configuration
    if config_name is None:
        config_name = os.getenv('FLASK_CONFIG', 'default')
    
    app.config.from_object(config[config_name])

    # Initialize extensions
    db.init_app(app)
    bcrypt.init_app(app)
    api = Api(app, version='1.0', title='HBnB API', description='HBnB Application API')

    # Import and register namespaces
    from app.api.v1.users import api as users_ns
    from app.api.v1.amenities import api as amenities_ns
    from app.api.v1.places import api as places_ns

    api.add_namespace(users_ns, path='/api/v1/users')
    api.add_namespace(amenities_ns, path='/api/v1/amenities')
    api.add_namespace(places_ns, path='/api/v1/places')

    return app
