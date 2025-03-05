from app.models.user import User
from app import db
from sqlalchemy.exc import IntegrityError

class UserService:


    @staticmethod
    def create_user(name: str, email: str, password: str):
        try:
            user = User(full_name=name, email=email, password=password)
            db.session.add(user)
            db.session.commit()
            return {'message': 'User created successfully'}, 201
        except IntegrityError:
            return {'message': 'Email already registered'}, 400


    @staticmethod
    def get_all_users(page: int, per_page: int):
        users = User.query.paginate(page=page, per_page=per_page, error_out=False)
        return {
            'users': [user.to_dict() for user in users.items],
            'total': users.total,
            'pages': users.pages
        }, 200


    @staticmethod
    def get_user(user_id: int):
        user = User.query.get(user_id)
        if user:
            return {'user': user.to_dict()}, 200
        return {'message': 'User not found'}, 404
