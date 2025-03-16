from flask import request, jsonify
from app.services import OrderService
from app.utils.logger import logger
from . import order_bp

# Order Routes
@order_bp.route('/order', methods=['POST'])
def create_order():
    data = request.get_json()
    try:
        order = OrderService.create_order(
            user_id=data['user_id'],
            user_address=data['user_address'],
            status=data.get('status', 'pending'),
            payment_transaction_id=data.get('payment_transaction_id')
        )
        return jsonify(order.to_dict()), 201
    except Exception as e:
        logger.error(f"Order creation error: {e}")
        return jsonify({'error': str(e)}), 400


@order_bp.route('/order/<int:order_id>', methods=['PUT'])
def update_order(order_id):
    data = request.get_json()
    try:
        order = OrderService.update_order(
            order_id=order_id,
            status=data.get('status'),
            user_address=data.get('user_address'),
            payment_transaction_id=data.get('payment_transaction_id')
        )
        return jsonify(order.to_dict()), 200
    except Exception as e:
        logger.error(f"Order update error: {e}")
        return jsonify({'error': str(e)}), 400


@order_bp.route('/order/<int:order_id>', methods=['GET'])
def get_order_by_id(order_id):
    try:
        order = OrderService.get_order_by_id(order_id)
        return jsonify(order.to_dict()), 200
    except Exception as e:
        logger.error(f"Order retrieval error: {e}")
        return jsonify({'error': str(e)}), 404


@order_bp.route('/orders/user/<int:user_id>', methods=['GET'])
def get_orders_by_user(user_id):
    try:
        orders = OrderService.get_orders_by_user(user_id)
        return jsonify([order.to_dict() for order in orders]), 200
    except Exception as e:
        logger.error(f"Order retrieval error for user {user_id}: {e}")
        return jsonify({'error': str(e)}), 404
