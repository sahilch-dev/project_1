from flask import Blueprint

users_bp = Blueprint('users', __name__)
categories_bp = Blueprint('categories', __name__)

from .users import *
from .auth import *
from .category import *