#!/usr/bin/env python3
# Routes for item catelog api v1

# import Blueprint from Flask library for creating routes
from flask import Blueprint
# import request / response helpers from Flask
from flask import flash, jsonify, redirect, render_template, request, url_for
# import session helpers from flask
from flask import session
# SQLAlchemy imports
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# import database schema for SQLAlchemy
from db_configuration import Base, Category, Item

apiv1_routes = Blueprint("apiv1_routes", __name__)

engine = create_engine("sqlite:///catelog.db")
Base.metadata.bind = engine
dbSession = sessionmaker(bind=engine)
transaction = dbSession()


@apiv1_routes.route("/categories", methods=["GET"])
def CategoriesJson():
    """Return all categories with items"""
    categories = transaction.query(Category).join("items").all()
    return jsonify(Categories=[c.serializable for c in categories])


@apiv1_routes.route("/categories/<int:id>", methods=["GET"])
def CategoryJson(id):
    """Return specific category with items"""
    category = (transaction.query(Category).filter(Category.id == id)
                  .join("items").one())
    return jsonify(Category=category.serializable)


@apiv1_routes.route("/items", methods=["GET"])
def ItemsJson():
    """Return all items"""
    items = transaction.query(Item).all()
    return jsonify(Items=[i.serializable for i in items])


@apiv1_routes.route("/items/<int:id>", methods=["GET"])
def ItemJson(id):
    """Return specific item"""
    item = transaction.query(Item).filter(Item.id == id).one()
    return jsonify(Item=item.serializable)


# prevent file from attempting to run alone
if(__name__ == "__main__"):
    print("This file cannot be run directly")
