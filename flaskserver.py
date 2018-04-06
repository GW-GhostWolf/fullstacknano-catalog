#!/usr/bin/env python3
# Web server for categories application using flask

from flask import Flask, jsonify, render_template, request
import json

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from db_configuration import Base, Category, Item

app = Flask(__name__)
engine = create_engine("sqlite:///categlog.db")
Base.metadata.bind = engine
dbSession = sessionmaker(bind=engine)
session = dbSession()


@app.route("/")
@app.route("/categories", methods=["GET"])
def getCategories():
    categories = session.query(Category)\
            .join("items")\
            .all()
    return render_template("categories.html", categories=categories)


@app.route("/category/<int:catId>/newItem", methods=["GET", "POST"])
def newItem(catId):
    if request.method == 'POST':
        # TODO - save the new item
        ""
    else:
        category = session.query(Category).filter(Category.id==catId).one()
        item = Item(id=0, name="", description="", cat_id=category.id)
        return render_template("editItem.html", category=category, item=item)


@app.route("/item/<int:itemId>", methods=["GET"])
def viewItem(itemId):
    item = session.query(Item).join("category").filter(Item.id==itemId).one()
    return render_template("item.html", item=item)


@app.route("/item/<int:itemId>/edit", methods=["GET", "POST"])
def editItem(itemId):
    if request.method == 'POST':
        # TODO - save the updates to the existing item
        ""
    else:
        item = (session.query(Item).join("category")
            .filter(Item.id==itemId).one())
        return render_template("editItem.html",
            category=item.category, item=item)


@app.route("/item/<int:itemId>/delete", methods=["GET", "POST"])
def deleteItem(itemId):
    if request.method == 'POST':
        # TODO - delete the item
        ""
    else:
        item = (session.query(Item).join("category")
            .filter(Item.id==itemId).one())
        return render_template("deleteItem.html", item=item)


@app.route("/categories.json", methods=["GET"])
def CategoryJson():
    categories = session.query(Category).join("items").all()
    return jsonify(Categories=[c.serializable for c in categories])


if(__name__ == "__main__"):
    app.debug = True
    app.run(host='0.0.0.0', port=5000)