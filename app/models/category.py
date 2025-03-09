from app import db
from sqlalchemy import Column, Integer, String, ForeignKey, func
from sqlalchemy.orm import relationship, Mapped


class Category(db.Model):
    __tablename__ = 'categories'

    id: Mapped[int] = Column(Integer, primary_key=True)
    name: Mapped[str] = Column(String, unique=True, nullable=False)
    created_at: Mapped[str] = Column(String, default=func.current_timestamp())
    updated_at: Mapped[str] = Column(String, default=func.current_timestamp(), onupdate=func.current_timestamp())

    parent_id: Mapped[int] = Column(
        Integer,
        ForeignKey('categories.id'),
        nullable=True,
    )

    parent = relationship('Category', remote_side=[id], backref='subcategories')

    def __init__(self, name, parent_id=None):
        self.name = name
        self.parent_id = parent_id

    def __repr__(self):
        return f'<Category(id={self.id}, name="{self.name}")>'

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'parent_id': self.parent_id
        }
