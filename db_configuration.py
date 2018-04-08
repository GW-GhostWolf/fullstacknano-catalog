#!/usr/bin/env python3
# Configure SQLAlchemy ORM and create the database

from sqlalchemy import create_engine, Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class User(Base):
    """Create user table for storing user information"""
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    email = Column(String(256), nullable=False)
    name = Column(String(256), nullable=False)


class Category(Base):
    """Create the table that will store the category information"""
    __tablename__ = "categories"
    id = Column(Integer, primary_key=True)
    name = Column(String(128), nullable=False)
    items = relationship("Item")
    user_id = Column(Integer, ForeignKey("users.id"))

    @property
    def serializable(self):
        """Return object data in easily serializeable format"""
        return {
            "id": self.id,
            "name": self.name,
            "items": [i.serializable for i in self.items],
            "userid": self.user_id
        }


class Item(Base):
    """Create the table that will store the item information"""
    __tablename__ = "items"
    id = Column(Integer, primary_key=True)
    name = Column(String(128), nullable=False)
    description = Column(String(512))
    cat_id = Column(Integer, ForeignKey("categories.id"))
    category = relationship(Category, back_populates="items")
    user_id = Column(Integer, ForeignKey("users.id"))

    @property
    def serializable(self):
        """Return object data in easily serializeable format"""
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "userid": self.user_id
        }


engine = create_engine("sqlite:///catelog.db")
Base.metadata.create_all(engine)
