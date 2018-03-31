#!/usr/bin/env python3
# Configurat SQLAlchemy ORM and create the database

import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()


class Category(Base):
    """Create the table that will store the category information"""
    __tablename__ = "categories"
    id = Column(Integer, primary_key = True)
    name = Column(String(128), nullable = False)


class Item(Base):
    """Create the table that will store the item information"""
    __tablename__ = "items"
    id = Column(Integer, primary_key = True)
    name = Column(String(128), nullable = False)
    description = Column(String(512))
    cat_id = Column(Integer, ForeignKey("categories.id"))
    category = relationship(Category)


engine = create_engine("sqlite:///categlog.db")
Base.metadata.create_all(engine)
