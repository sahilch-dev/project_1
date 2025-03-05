from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, func
from sqlalchemy.orm import Mapped

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'

    id: Mapped[int] = Column(Integer, primary_key=True)
    full_name: Mapped[str] = Column(String)
    email: Mapped[str] = Column(String, unique=True)
    password: Mapped[str] = Column(String)
    created_at: Mapped[str] = Column(String, default=func.current_timestamp())
    updated_at: Mapped[str] = Column(String, default=func.current_timestamp(), onupdate=func.current_timestamp())

    def __init__(self, full_name: str, email: str, password: str):
        self.full_name = full_name
        self.email = email
        self.password = password

    def __repr__(self):
        return f'<User(id={self.id}, full_name="{self.full_name}", email="{self.email}")>'

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.full_name,
            'email': self.email
        }
