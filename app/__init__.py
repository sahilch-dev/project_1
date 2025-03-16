import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.log import echo_property

db = SQLAlchemy()

def create_app() -> Flask:
    app = Flask(__name__)

    # Load configuration from config.py
    app.config.from_object('app.config.Config')
    db.init_app(app)

    from app.routes import users_bp, categories_bp, cart_bp, products_bp, admin_bp

    app.register_blueprint(cart_bp, url_prefix='/api/v1/cart')
    app.register_blueprint(products_bp, url_prefix='/api/v1/products')
    app.register_blueprint(users_bp, url_prefix='/api/v1/users')
    app.register_blueprint(categories_bp, url_prefix='/api/v1/categories')
    app.register_blueprint(admin_bp, url_prefix='/api/v1/admin')

    with app.app_context():
        db.drop_all()
        db.create_all()
    return app
