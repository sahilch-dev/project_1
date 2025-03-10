import jwt
from datetime import datetime, timedelta, timezone
from flask import current_app
from werkzeug.security import generate_password_hash, check_password_hash
from app.models.user import User
from app import db
from app.utils.logger import logger

class AuthService:

    @staticmethod
    def register_user(name, email, password):
        hashed_password = generate_password_hash(password)
        user = User(full_name=name, email=email, password=hashed_password)
        try:
            db.session.add(user)
            db.session.commit()
            return {'message': 'User registered successfully'}, 201
        except Exception as e:
            logger.error(f"Error registering user: {e}")
            return {'message': 'Email already exists'}, 400

    @staticmethod
    def login_user(email, password):
        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password, password):
            token = jwt.encode(
                {'id': user.id, 'exp': datetime.now(timezone.utc) + timedelta(hours=1)},
                current_app.config['JWT_SECRET_KEY'],
                algorithm="HS256"
            )
            return {'token': token}, 200
        return {'message': 'Invalid credentials'}, 401