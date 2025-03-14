from flask import request, make_response
from app.services import ProductService
from app.utils.validator import ProductSchema
from app.routes import products_bp


@products_bp.route('', methods=['GET'])
def get_all_products():
    product_name = request.args.get('product_name', None)

    response, status = ProductService.get_all_products(product_name)
    return make_response(response, status)

@products_bp.route('/<int:product_id>', methods=['GET'])
def get_product(product_id):
    response, status = ProductService.get_product_by_id(product_id)
    return make_response(response, status)

@products_bp.route('', methods=['POST'])
def create_product():
    data = request.get_json()
    errors = ProductSchema().validate(data)
    if errors:
        return make_response({'errors': errors}, 400)
    response, status = ProductService.create_product(data)
    return make_response(response, status)

@products_bp.route('/<int:product_id>', methods=['PUT'])
def update_product(product_id):
    data = request.get_json()
    response, status = ProductService.update_product(product_id, data)
    return make_response(response, status)

@products_bp.route('/<int:product_id>', methods=['DELETE'])
def delete_product(product_id):
    response, status = ProductService.delete_product(product_id)
    return make_response(response, status)