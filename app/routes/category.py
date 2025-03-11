from flask import request, jsonify
from . import categories_bp
from app.services import CategoryService
from app.utils.validator import CategorySchema

category_schema = CategorySchema()
category_list_schema = CategorySchema(many=True)

@categories_bp.get('')
def get_categories():
    return CategoryService.get_all_categories()

@categories_bp.get('/<int:category_id>')
def get_category(category_id):
    return CategoryService.get_category_by_id(category_id)

@categories_bp.post('')
def create_category():
    data = request.json

    errors = category_schema.validate(data)
    if errors:
        return jsonify(errors), 400
    return CategoryService.create_category(data)

@categories_bp.put('/<int:category_id>')
def update_category(category_id):
    data = request.json
    errors = category_schema.validate(data, partial=True)  # Allow partial updates
    if errors:
        return jsonify(errors), 400

    return CategoryService.update_category(category_id, data)

@categories_bp.delete('/<int:category_id>')
def delete_category(category_id: int):
    return CategoryService.delete_category(category_id)
