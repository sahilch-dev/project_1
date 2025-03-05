from flask import request, make_response
from app.services.user_service import UserService
from . import users_bp

@users_bp.route('/', methods=['POST'])
def create_user():
    data = request.get_json()
    response, status = UserService.create_user(data.get('name'), data.get('email'), data.get('password'))
    return make_response(response, status)

@users_bp.route('/', methods=['GET'])
def get_all_users():
    response, status = UserService.get_all_users()
    return make_response(response, status)

@users_bp.route('/<int:user_id>', methods=['GET'])
def get_user(user_id: int):
    response, status = UserService.get_user(user_id)
    return make_response(response, status)
