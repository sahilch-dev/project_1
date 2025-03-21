from typing import List
from sqlalchemy import (
    Column,
    Integer,
    Float,
    String,
    Boolean,
    ForeignKey,
    func
)
from sqlalchemy.orm import relationship, Mapped
from app import db


class Product(db.Model):
    __tablename__ = 'products'
    id: Mapped[int] = Column(Integer, primary_key=True)
    name: Mapped[str] = Column(String, unique=True, nullable=False)
    description: Mapped[str] = Column(String, nullable=True)
    price: Mapped[float] = Column(Float, nullable=False)
    stock: Mapped[int] = Column(Integer, nullable=False, default=0)
    image_url: Mapped[str] = Column(String, nullable=True)
    category_id: Mapped[int] = Column(Integer, ForeignKey('categories.id'), nullable=False)

    def __repr__(self):
        return f'<Product(id={self.id}, name="{self.name}", price={self.price})>'

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'price': self.price,
            'stock': self.stock,
            'image_url': self.image_url,
            'category_id': self.category_id
        }


class Category(db.Model):
    __tablename__ = 'categories'
    id: Mapped[int] = Column(Integer, primary_key=True)
    name: Mapped[str] = Column(String, unique=True, nullable=False)
    parent_id: Mapped[int] = Column(
        Integer,
        ForeignKey('categories.id'),
        nullable=True,
    )
    parent = relationship('Category', remote_side=[id], backref='subcategories')

    created_at: Mapped[str] = Column(String, default=func.current_timestamp())
    updated_at: Mapped[str] = Column(String, default=func.current_timestamp(), onupdate=func.current_timestamp())

    def __repr__(self):
        return f'<Category(id={self.id}, name="{self.name}")>'

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'parrent': self.parent_id,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }


class User(db.Model):
    __tablename__ = 'users'
    id: Mapped[int] = Column(Integer, primary_key=True)
    full_name: Mapped[str] = Column(String)
    email: Mapped[str] = Column(String, unique=True)
    password: Mapped[str] = Column(String)
    created_at: Mapped[str] = Column(String, default=func.current_timestamp())
    updated_at: Mapped[str] = Column(String, default=func.current_timestamp(), onupdate=func.current_timestamp())

    def __repr__(self):
        return f'<User(id={self.id}, email="{self.email}")>'

    def to_dict(self):
        return {
            'id': self.id,
            'full_name': self.full_name,
            'email': self.email,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }

class Admin(db.Model):
    __tablename__ = 'admin'
    id: Mapped[int] = Column(Integer, primary_key=True)
    full_name: Mapped[str] = Column(String)
    email: Mapped[str] = Column(String, unique=True)
    password: Mapped[str] = Column(String)
    active: Mapped[bool] = Column(Boolean, default=True)
    created_at: Mapped[str] = Column(String, default=func.current_timestamp())
    updated_at: Mapped[str] = Column(String, default=func.current_timestamp(), onupdate=func.current_timestamp())

    def __repr__(self):
        return f'<User(id={self.id}, email="{self.email}")>'

    def to_dict(self):
        return {
            'id': self.id,
            'full_name': self.full_name,
            'email': self.email,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }


class UserAddress(db.Model):
    __tablename__ = 'user_addresses'
    id: Mapped[int] = Column(Integer, primary_key=True)
    user_id: Mapped[int] = Column(Integer, ForeignKey('users.id'), nullable=False)
    contact_number: Mapped[str] = Column(String, nullable=False)
    address_line1: Mapped[str] = Column(String, nullable=False)
    address_line2: Mapped[str] = Column(String, nullable=True)
    address_line3: Mapped[str] = Column(String, nullable=True)
    pincode: Mapped[str] = Column(String, nullable=False)
    landmark: Mapped[str] = Column(String, nullable=True)
    state: Mapped[str] = Column(String, nullable=False)

    def __repr__(self):
        return f'<UserAddress(id={self.id}, user_id={self.user_id})>'

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'contact_number': self.contact_number,
            'address_line1': self.address_line1,
            'address_line2': self.address_line2,
            'address_line3': self.address_line3,
            'pincode': self.pincode,
            'landmark': self.landmark,
            'state': self.state
        }


class Cart(db.Model):
    __tablename__ = 'carts'
    id: Mapped[int] = Column(Integer, primary_key=True)
    user_id: Mapped[int] = Column(Integer, ForeignKey('users.id'), nullable=False)
    product_id: Mapped[int] = Column(Integer, ForeignKey('products.id'), nullable=False)
    quantity: Mapped[int] = Column(Integer, nullable=False, default=1)

    def __repr__(self):
        return f'<Cart(id={self.id}, user_id={self.user_id}, product_id={self.product_id})>'

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'product_id': self.product_id,
            'quantity': self.quantity
        }


class PaymentTransaction(db.Model):
    __tablename__ = 'payment_transactions'
    id: Mapped[int] = Column(Integer, primary_key=True)
    transaction_id: Mapped[str] = Column(String, unique=True, nullable=False)
    order_id: Mapped[int] = Column(Integer, ForeignKey('orders.id'), nullable=False)
    amount: Mapped[float] = Column(Float, nullable=False)
    status: Mapped[str] = Column(String, nullable=False)
    payment_method: Mapped[str] = Column(String, nullable=False)
    created_at: Mapped[str] = Column(String, default=func.current_timestamp())
    updated_at: Mapped[str] = Column(String, default=func.current_timestamp(), onupdate=func.current_timestamp())

    order = relationship('Order', backref='payment_transactions')

    def __repr__(self):
        return f'<PaymentTransaction(id={self.id}, transaction_id="{self.transaction_id}", amount={self.amount}, status="{self.status}")>'

    def to_dict(self):
        return {
            'id': self.id,
            'transaction_id': self.transaction_id,
            'order_id': self.order_id,
            'amount': self.amount,
            'status': self.status,
            'payment_method': self.payment_method,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }


class Order(db.Model):
    __tablename__ = 'orders'
    id: Mapped[int] = Column(Integer, primary_key=True)
    user_id: Mapped[int] = Column(Integer, ForeignKey('users.id'), nullable=False)
    user_address: Mapped[int] = Column(Integer, ForeignKey('user_addresses.id'), nullable=False)
    total_amount: Mapped[float] = Column(Float, nullable=False)
    status: Mapped[str] = Column(String, nullable=False)
    payment_transaction_id: Mapped[int] = Column(Integer, ForeignKey('payment_transactions.id'), nullable=True)
    created_at: Mapped[str] = Column(String, default=func.current_timestamp())
    updated_at: Mapped[str] = Column(String, default=func.current_timestamp(), onupdate=func.current_timestamp())

    user = relationship('User', backref='orders')
    payment_transaction = relationship('PaymentTransaction', backref='order', uselist=False)
    items = relationship('OrderItem', backref='order', cascade='all, delete-orphan')

    def __repr__(self):
        return f'<Order(id={self.id}, user_id={self.user_id}, status="{self.status}")>'

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'total_amount': self.total_amount,
            'status': self.status,
            'payment_transaction_id': self.payment_transaction_id,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
            'items': [item.to_dict() for item in self.items]
        }

class OrderItem(db.Model):
    __tablename__ = 'order_items'
    id: Mapped[int] = Column(Integer, primary_key=True)
    order_id: Mapped[int] = Column(Integer, ForeignKey('orders.id'), nullable=False)
    product_id: Mapped[int] = Column(Integer, ForeignKey('products.id'), nullable=False)
    quantity: Mapped[int] = Column(Integer, nullable=False)
    price: Mapped[float] = Column(Float, nullable=False)
    subtotal: Mapped[float] = Column(Float, nullable=False)

    product = relationship('Product')

    def __repr__(self):
        return f'<OrderItem(id={self.id}, order_id={self.order_id}, product_id={self.product_id}, quantity={self.quantity})>'

    def to_dict(self):
        return {
            'id': self.id,
            'order_id': self.order_id,
            'product_id': self.product_id,
            'quantity': self.quantity,
            'price': self.price,
            'subtotal': self.subtotal
        }
