from flask import jsonify
from app import db
from app.models.category import Category

class CategoryService:

    @staticmethod
    def get_all_categories():
        categories = Category.query.all()
        return jsonify([category.to_dict() for category in categories]), 200

    @staticmethod
    def get_category_by_id(category_id):
        category = Category.query.get(category_id)
        if not category:
            return jsonify({'error': 'Category not found'}), 404
        return jsonify(category.to_dict()), 200

    @staticmethod
    def create_category(data):
        name = data.get('name')
        parent_id = data.get('parent_id')

        if not name:
            return jsonify({'error': 'Name is required'}), 400

        new_category = Category(name=name, parent_id=parent_id)
        db.session.add(new_category)
        db.session.commit()

        return jsonify(new_category.to_dict()), 201

    @staticmethod
    def update_category(category_id, data):
        category = Category.query.get(category_id)
        if not category:
            return jsonify({'error': 'Category not found'}), 404

        category.name = data.get('name', category.name)
        category.parent_id = data.get('parent_id', category.parent_id)

        db.session.commit()
        return jsonify(category.to_dict()), 200

    @staticmethod
    def delete_category(category_id):
        category = Category.query.get(category_id)
        if not category:
            return jsonify({'error': 'Category not found'}), 404

        db.session.delete(category)
        db.session.commit()
        return jsonify({'message': 'Category deleted successfully'}), 200