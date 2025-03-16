from flask import request, make_response
from app.services import AdminService
from . import admin_bp


@admin_bp.post('')
def create_user():
    print("get_hit")
    data = request.get_json()
    response, status = AdminService.create_user(data.get('name'), data.get('email'), data.get('password'))
    return make_response(response, status)

@admin_bp.get('')
def get_all_users():
    page = request.args.get('page', default=1, type=int)
    per_page = request.args.get('per_page', default=10, type=int)

    response, status = AdminService.get_all_users(page, per_page)
    return make_response(response, status)

@admin_bp.get('/<int:user_id>')
def get_user(user_id: int):
    response, status = AdminService.get_user(user_id)
    return make_response(response, status)
