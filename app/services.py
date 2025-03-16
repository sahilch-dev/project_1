from datetime import datetime, timedelta, timezone
from functools import wraps
from flask import current_app, request, jsonify, g
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.exc import IntegrityError
import jwt

from app.models import ( Product, Category, Cart, User, UserAddress, Admin, )
from app import db
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
    def disable_user(user_id):
        pass

    @staticmethod
    def enable_user(user_id):
        pass


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
