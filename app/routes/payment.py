from flask import request, jsonify
from app.services import PaymentTransactionService
from app.utils.logger import logger
from . import payment_bp




# Payment Routes
@payment_bp.route('/payment', methods=['POST'])
def create_payment():
    data = request.get_json()
    try:
        transaction = PaymentTransactionService.create_transaction(
            transaction_id=data['transaction_id'],
            amount=data['amount'],
            status=data['status'],
            payment_method=data['payment_method'],
            order_id=data['order_id']
        )
        return jsonify(transaction.to_dict()), 201
    except Exception as e:
        logger.error(f"Payment creation error: {e}")
        return jsonify({'error': str(e)}), 400


@payment_bp.route('/payment/<transaction_id>', methods=['PUT'])
def update_payment(transaction_id):
    data = request.get_json()
    try:
        transaction = PaymentTransactionService.update_transaction(
            transaction_id=transaction_id,
            amount=data.get('amount'),
            status=data.get('status'),
            payment_method=data.get('payment_method')
        )
        return jsonify(transaction.to_dict()), 200
    except Exception as e:
        logger.error(f"Payment update error: {e}")
        return jsonify({'error': str(e)}), 400
