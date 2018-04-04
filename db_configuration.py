#!/usr/bin/env python3
# Configure SQLAlchemy ORM and create the database

from sqlalchemy import create_engine, Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class Category(Base):
    """Create the table that will store the category information"""
    __tablename__ = "categories"
    id = Column(Integer, primary_key=True)
    name = Column(String(128), nullable=False)
    items = relationship("Item")
    @property
    def serializable(self):
        """Return object data in easily serializeable format"""
        return {
            "id": self.id,
            "name": self.name,
            "items": [i.serializable for i in self.items]
        }


class Item(Base):
    """Create the table that will store the item information"""
    __tablename__ = "items"
    id = Column(Integer, primary_key=True)
    name = Column(String(128), nullable=False)
    description = Column(String(512))
    cat_id = Column(Integer, ForeignKey("categories.id"))
    category = relationship(Category, back_populates="items")
    @property
    def serializable(self):
        """Return object data in easily serializeable format"""
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description
        }


engine = create_engine("sqlite:///categlog.db")
Base.metadata.create_all(engine)
