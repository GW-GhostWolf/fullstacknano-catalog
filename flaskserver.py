#!/usr/bin/env python3
# Web server for categories application using flask

from flask import Flask, jsonify, redirect, render_template, request, url_for
import json

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from db_configuration import Base, Category, Item

app = Flask(__name__)
engine = create_engine("sqlite:///categlog.db")
Base.metadata.bind = engine
dbSession = sessionmaker(bind=engine)
session = dbSession()


@app.route("/", methods=["GET"])
@app.route("/categories", methods=["GET"])
def getCategories():
    categories = session.query(Category).outerjoin("items").all()
    return render_template("categories.html", categories=categories)


@app.route("/category/<int:catId>/newItem", methods=["GET", "POST"])
def newItem(catId):
    if request.method == "POST":
        newItem = Item(name=request.form["name"],
            description=request.form["description"],
            cat_id=catId)
        session.add(newItem)
        session.commit()
        return redirect(url_for("viewItem", itemId=newItem.id))
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
    item = session.query(Item).join("category").filter(Item.id==itemId).one()
    if request.method == "POST":
        item.name = request.form["name"]
        item.description = request.form["description"]
        session.commit()
        return redirect(url_for("viewItem", itemId=itemId))
    else:
        return render_template("editItem.html",
            category=item.category, item=item)


@app.route("/item/<int:itemId>/delete", methods=["GET", "POST"])
def deleteItem(itemId):
    item = session.query(Item).join("category").filter(Item.id==itemId).one()
    if request.method == "POST":
        session.delete(item)
        session.commit()
        return redirect(url_for("getCategories"))
    else:
        return render_template("deleteItem.html", item=item)


@app.route("/categories.json", methods=["GET"])
def CategoryJson():
    categories = session.query(Category).join("items").all()
    return jsonify(Categories=[c.serializable for c in categories])


if(__name__ == "__main__"):
    app.debug = True
    app.run(host="0.0.0.0", port=5000)