# app/__init__.py

from flask import Flask
from flask_restx import Api
from flask_sqlalchemy import SQLAlchemy
import os

db = SQLAlchemy()

def create_app(config_name=None):
    app = Flask(__name__)
    
    from config import config
    
    if config_name is None:
        config_name = os.getenv('FLASK_CONFIG', 'default')
    
    app.config.from_object(config[config_name])

    db.init_app(app)
    api = Api(app, version='1.0', title='HBnB API', description='HBnB Application API')

    from app.api.v1.users import api as users_ns
    from app.api.v1.amenities import api as amenities_ns
    from app.api.v1.places import api as places_ns

    api.add_namespace(users_ns, path='/api/v1/users')
    api.add_namespace(amenities_ns, path='/api/v1/amenities')
    api.add_namespace(places_ns, path='/api/v1/places')

    return app
