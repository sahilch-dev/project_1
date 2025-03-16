from datetime import datetime, timedelta, timezone
from functools import wraps

import jwt
from flask import current_app, request, jsonify, g
from sqlalchemy.exc import IntegrityError
from sqlalchemy.exc import SQLAlchemyError
from werkzeug.security import generate_password_hash, check_password_hash

from app import db
from app.models import (Product, Category, Cart, User, UserAddress, Admin, Order, OrderItem, PaymentTransaction)
from app.utils.logger import logger


class CategoryService:

    @staticmethod
    def get_all_categories():
        categories = Category.query.all()
        return [category.to_dict() for category in categories], 200


    @staticmethod
    def get_category_by_id(category_id):
        category = Category.query.get(category_id)
        if not category:
            return {'error': 'Category not found'}, 200
        return category.to_dict(), 200

    @staticmethod
    def get_category_by_name(category_name):
        categories = Category.query.filter(Category.name.ilike(f'%{category_name}%')).all()
        return [category.to_dict() for category in categories], 200

    @staticmethod
    def create_category(data):
        name = data.get('name')
        parent_id = data.get('parent_id', None)

        if not name:
            return {'error': 'Name is required'}

        new_category = Category(name=name, parent_id=parent_id)

        try:
            db.session.add(new_category)
            db.session.commit()
            return new_category.to_dict(), 201

        except IntegrityError:
            db.session.rollback()
            return {'error': 'Category with the same name already exists'}, 400


    @staticmethod
    def update_category(category_id, data):
        category = Category.query.get(category_id)
        if not category:
            return {'error': 'Category not found'}

        category.name = data.get('name', category.name)
        category.parent_id = data.get('parent_id', category.parent_id)

        db.session.commit()
        return category.to_dict(), 201


    @staticmethod
    def delete_category(category_id):
        category = Category.query.get(category_id)
        if not category:
            return {'error': 'Category not found'}, 400

        db.session.delete(category)
        db.session.commit()
        return {'message': 'Category deleted successfully'}, 204


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

    @staticmethod
    def admin_auth(email, password):
        user = Admin.query.filter_by(email=email).first()
        if user and user.password == password:
            token = jwt.encode(
                {'id': user.id, 'user': "admin", 'exp': datetime.now(timezone.utc) + timedelta(hours=1)},
                current_app.config['JWT_SECRET_KEY'],
                algorithm="HS256"
            )
            return {'token': token}, 200
        return {'message': 'Invalid credentials'}, 401


    @staticmethod
    def token_required(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            token = None

            if 'Authorization' in request.headers:
                token = request.headers['Authorization'].split(" ")[-1]

            if not token:
                return jsonify({'message': 'Token is missing!'}), 401

            try:
                data = jwt.decode(token, current_app.config['JWT_SECRET_KEY'], algorithms=["HS256"])
                current_user = User.query.get(data['id'])
                if not current_user:
                    return jsonify({'message': 'User not found!'}), 404
                g.current_user = current_user
            except jwt.ExpiredSignatureError:
                return jsonify({'message': 'Token has expired!'}), 401
            except jwt.InvalidTokenError:
                return jsonify({'message': 'Invalid token!'}), 401

            return f(*args, **kwargs)
        return decorated


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

class AdminService:

    @staticmethod
    def create_user(name: str, email: str, password: str):
        try:
            user = Admin(full_name=name, email=email, password=password)
            db.session.add(user)
            db.session.commit()
            return {'message': 'User created successfully'}, 201
        except IntegrityError:
            return {'message': 'Email already registered'}, 400

    @staticmethod
    def get_all_users(page: int, per_page: int):
        users = Admin.query.paginate(page=page, per_page=per_page, error_out=False)
        return {
            'users': [user.to_dict() for user in users.items],
            'total': users.total,
            'pages': users.pages
        }, 200

    @staticmethod
    def get_user(user_id: int):
        user = Admin.query.get(user_id)
        if user:
            return {'user': user.to_dict()}, 200
        return {'message': 'User not found'}, 404

    @staticmethod
    def update_user(user_id, data):
        admin = Admin.query.get(user_id)
        if not admin:
            return {'error': 'Admin not found'}, 404

        for field in ['full_name', 'email', 'password', 'active']:
            if field in data:
                setattr(admin, field, data[field])
        db.session.commit()
        return admin.to_dict(), 200


class ProductService:

    @staticmethod
    def get_all_products(product_name):
        products = []
        products = Product.query.all()
        return [product.to_dict() for product in products], 200

    @staticmethod
    def get_product_by_name(product_name):
        products = Product.query.filter(Product.name.ilike(f'%{product_name}%')).all()
        return [product.to_dict() for product in products], 200

    @staticmethod
    def get_product_by_category(category_name):
        response, status = CategoryService.get_category_by_name(category_name)
        category_id = response[0].id
        products = Product.query.filter(Product.category_id == category_id).all()
        return [product.to_dict() for product in products], 200

    @staticmethod
    def get_product_by_id(product_id):
        product = Product.query.get(product_id)
        if not product:
            return {'error': 'Product not found'}, 404
        return product.to_dict(), 200

    @staticmethod
    def create_product(data):
        try:
            # Ensuring all required fields are present
            product = Product(
                name=data.get('name'),
                description=data.get('description'),
                price=data.get('price'),
                stock=data.get('stock', 0),
                image_url=data.get('image_url'),
                category_id=data.get('category_id')
            )
            db.session.add(product)
            db.session.commit()
            return product.to_dict(), 201
        except IntegrityError as e:
            db.session.rollback()
            logger.error(f"Error creating product: {e}")
            return {'error': 'Product creation failed due to integrity error'}, 400
        except Exception as e:
            db.session.rollback()
            logger.error(f"Unexpected error creating product: {e}")
            return {'error': 'Unexpected error occurred'}, 500

    @staticmethod
    def update_product(product_id, data):
        product = Product.query.get(product_id)
        if not product:
            return {'error': 'Product not found'}, 404

        # Only update fields that are present in the data
        for field in ['name', 'description', 'price', 'stock', 'image_url', 'category_id']:
            if field in data:
                setattr(product, field, data[field])
        db.session.commit()
        return product.to_dict(), 200

    @staticmethod
    def delete_product(product_id):
        product = Product.query.get(product_id)
        if not product:
            return {'error': 'Product not found'}, 404
        db.session.delete(product)
        db.session.commit()
        return {'message': 'Product deleted successfully'}, 204

class CartService:

    @staticmethod
    def add_to_cart(user_id, product_id, quantity):
        cart_item = Cart(user_id=user_id, product_id=product_id, quantity=quantity)
        db.session.add(cart_item)
        db.session.commit()
        return cart_item.to_dict(), 201

    @staticmethod
    def get_user_cart(user_id):
        items = Cart.query.filter_by(user_id=user_id).all()
        return [item.to_dict() for item in items], 200

    @staticmethod
    def remove_from_cart(cart_id):
        cart_item = Cart.query.get(cart_id)
        if not cart_item:
            return {'error': 'Item not found in cart'}, 404
        db.session.delete(cart_item)
        db.session.commit()
        return {'message': 'Item removed from cart'}, 200

    @staticmethod
    def update_cart_item(cart_id, quantity):
        cart_item = Cart.query.get(cart_id)
        if not cart_item:
            return {'error': 'Item not found in cart'}, 404
        cart_item.quantity = quantity
        db.session.commit()
        return cart_item.to_dict(), 200


class AddressService:

    @staticmethod
    def add_address(user_id, data):
        address = UserAddress(user_id=user_id, **data)
        db.session.add(address)
        db.session.commit()
        return address.to_dict(), 201

    @staticmethod
    def get_user_addresses(user_id):
        addresses = UserAddress.query.filter_by(user_id=user_id).all()
        return [address.to_dict() for address in addresses], 200


class PaymentTransactionService:

    @staticmethod
    def create_transaction(transaction_id: str, amount: float, status: str, payment_method: str,
                           order_id: int) -> PaymentTransaction:
        try:
            transaction = PaymentTransaction(
                transaction_id=transaction_id,
                amount=amount,
                status=status,
                payment_method=payment_method,
                order_id=order_id
            )
            db.session.add(transaction)
            db.session.commit()
            return transaction
        except SQLAlchemyError as e:
            db.session.rollback()
            raise Exception(f"Error creating payment transaction: {e}")

    @staticmethod
    def update_transaction(transaction_id: str, amount: float = None, status: str = None,
                           payment_method: str = None) -> PaymentTransaction:
        try:
            transaction = PaymentTransaction.query.filter_by(transaction_id=transaction_id).first()
            if not transaction:
                raise Exception(f"Transaction with ID '{transaction_id}' not found.")

            if amount is not None:
                transaction.amount = amount
            if status is not None:
                transaction.status = status
            if payment_method is not None:
                transaction.payment_method = payment_method

            db.session.commit()
            return transaction
        except SQLAlchemyError as e:
            db.session.rollback()
            raise Exception(f"Error updating payment transaction: {e}")


class OrderService:

    @staticmethod
    def create_order(user_id: int, user_address: int, status: str = "pending",
                     payment_transaction_id: int = None) -> Order:
        """
        Create a new order using the user's cart items, calculate total amount, and remove items from the cart.

        :param user_id: ID of the user placing the order.
        :param user_address: ID of the user's address.
        :param status: Initial status of the order.
        :param payment_transaction_id: Optional payment transaction ID.
        :return: Created Order instance.
        """
        try:
            # Fetch all cart items for the user
            cart_items = Cart.query.filter_by(user_id=user_id).all()
            if not cart_items:
                return {"message": "cart is empty"}, 200

            # Calculate total amount
            total_amount = sum(item.quantity * item.product.price for item in cart_items)

            # Create the order
            order = Order(
                user_id=user_id,
                user_address=user_address,
                total_amount=total_amount,
                status=status,
                payment_transaction_id=payment_transaction_id
            )
            db.session.add(order)
            db.session.flush()  # To get the order.id before committing

            # Add each cart item to the order and remove it from the cart
            for cart_item in cart_items:
                order_item = OrderItem(
                    order_id=order.id,
                    product_id=cart_item.product_id,
                    quantity=cart_item.quantity,
                    price=cart_item.product.price,
                    subtotal=cart_item.quantity * cart_item.product.price
                )
                db.session.add(order_item)
                db.session.delete(cart_item)

            db.session.commit()
            return order
        except SQLAlchemyError as e:
            db.session.rollback()
            raise Exception(f"Error creating order: {e}")

    @staticmethod
    def update_order(order_id: int, status: str = None, user_address: int = None, payment_transaction_id: int = None) -> Order:
        """
        Update an existing order's status, address, or payment transaction.

        :param order_id: ID of the order to update.
        :param status: New status of the order.
        :param user_address: New user address ID.
        :param payment_transaction_id: New payment transaction ID.
        :return: Updated Order instance.
        """
        try:
            order = Order.query.get(order_id)
            if not order:
                raise Exception(f"Order with ID '{order_id}' not found.")

            if status:
                order.status = status
            if user_address:
                order.user_address = user_address
            if payment_transaction_id:
                order.payment_transaction_id = payment_transaction_id

            db.session.commit()
            return order
        except SQLAlchemyError as e:
            db.session.rollback()
            raise Exception(f"Error updating order: {e}")

    @staticmethod
    def get_order_by_id(order_id: int) -> Order:
        """
        Retrieve an order by its ID.
        """
        order = Order.query.get(order_id)
        if not order:
            raise Exception(f"Order with ID '{order_id}' not found.")
        return order

    @staticmethod
    def get_orders_by_user(user_id: int) -> list:
        """
        Retrieve all orders for a specific user.
        """
        return Order.query.filter_by(user_id=user_id).all()
