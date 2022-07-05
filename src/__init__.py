from flask.json import jsonify
from flask import Flask, config, redirect
from src.users import users
from src.database import db
from flask_jwt_extended import JWTManager
import os


def create_app(test_config=None):

    app = Flask(__name__, instance_relative_config=True)

    if test_config is None:
        app.config.from_mapping(
            SECRET_KEY=os.environ.get("SECRET_KEY"),
            MONGODB_HOST=os.environ.get("MONGODB_HOST"),
            SQLALCHEMY_TRACK_MODIFICATIONS=False,
            JWT_SECRET_KEY=os.environ.get("JWT_SECRET_KEY"),
        )
    else:
        app.config.from_mapping(test_config)

    # Starting MYSQL database
    db.app = app
    db.init_app(app)

    # Init JWT for this application
    JWTManager(app)

    # Registering endpoints
    app.register_blueprint(users)

    return app
