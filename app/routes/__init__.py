from flask import Blueprint

users_bp = Blueprint('users', __name__)
admin_bp = Blueprint('admins', __name__)
categories_bp = Blueprint('categories', __name__)
cart_bp = Blueprint('cart', __name__)
products_bp = Blueprint('products', __name__)
files_bp = Blueprint('files', __name__)
payment_bp = Blueprint('payment', __name__)
order_bp = Blueprint('order', __name__)

from .users import *
from .auth import *
from .category import *
from .product import *
from .cart import *
from .admin import *
from .files import *
from .payment import *
from .order import *