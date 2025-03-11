from flask import request, make_response
from app.services import CartService
from app.utils.validator import CartSchema
from app.routes import cart_bp


@cart_bp.route('', methods=['POST'])
def add_to_cart():
    data = request.get_json()
    errors = CartSchema().validate(data)
    if errors:
        return make_response({'errors': errors}, 400)

    response, status = CartService.add_to_cart(data['user_id'], data['product_id'], data['quantity'])
    return make_response(response, status)

@cart_bp.route('/<int:user_id>', methods=['GET'])
def get_user_cart(user_id):
    response, status = CartService.get_user_cart(user_id)
    return make_response(response, status)

@cart_bp.route('/<int:cart_id>', methods=['DELETE'])
def remove_from_cart(cart_id):
    response, status = CartService.remove_from_cart(cart_id)
    return make_response(response, status)

@cart_bp.route('/<int:cart_id>', methods=['PUT'])
def update_cart(cart_id):
    data = request.get_json()
    response, status = CartService.update_cart_item(cart_id, data.get('quantity'))
    return make_response(response, status)
