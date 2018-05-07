# app/__init__.py

# Library imports
from flask_api import FlaskAPI
from flask_sqlalchemy import SQLAlchemy

# Local imports
from instance.config import app_config

# Initialize SQLAlchemy
db = SQLAlchemy()

def create_app(config_name):
    app = FlaskAPI(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

    return app
