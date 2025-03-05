import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app() -> Flask:
    app = Flask(__name__)

    # Load configuration from config.py
    app.config.from_object('app.config.Config')

    # Initialize extensions
    db.init_app(app)

    # Import and register Blueprints
    from app.routes import users_bp
    app.register_blueprint(users_bp, url_prefix='/users')

    return app
