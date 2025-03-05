from flask import Blueprint

users_bp = Blueprint('users', __name__)

from .users import *
from .auth import *