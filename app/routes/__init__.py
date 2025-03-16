from flask import Blueprint

users_bp = Blueprint('users', __name__)
admin_bp = Blueprint('admins', __name__)
categories_bp = Blueprint('categories', __name__)
cart_bp = Blueprint('cart', __name__)
products_bp = Blueprint('products', __name__)


from .users import *
from .auth import *
from .category import *
from .product import *
from .cart import *
from .admin import *