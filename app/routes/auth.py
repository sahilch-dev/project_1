from flask import request, make_response
from app.services import AuthService
from app.utils.validator import LoginSchema, UserSchema
from . import users_bp

@users_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    errors = UserSchema().validate(data)
    if errors:
        return make_response({"errors": errors}, 400)

    response, status = AuthService.register_user(data["name"], data["email"], data["password"])
    return make_response(response, status)

@users_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    errors = LoginSchema().validate(data)
    if errors:
        return make_response({"errors": errors}, 400)

    response, status = AuthService.login_user(data["email"], data["password"])
    return make_response(response, status)


@users_bp.route('/admin/login', methods=['POST'])
def login():
    data = request.get_json()
    errors = LoginSchema().validate(data)
    if errors:
        return make_response({"errors": errors}, 400)

    response, status = AuthService.admin_auth(data["email"], data["password"])
    return make_response(response, status)

