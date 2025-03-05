import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app() -> Flask:
    app = Flask(__name__)

    # Load configuration from config.py
    app.config.from_object('app.config.Config')
    db.init_app(app)

    from app.routes import users_bp
    app.register_blueprint(users_bp, url_prefix='/api/v1/users')

    return app
