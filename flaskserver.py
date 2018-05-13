#!/usr/bin/env python3
# Web server for categories application using Flask (http://flask.pocoo.org/)
# and SQLAlchemy (http://www.sqlalchemy.org/)

# import main Flask library
from flask import Flask
# import request / response helpers from Flask
from flask import jsonify, redirect, render_template, request, url_for
# import flash message and session helpers from Flask
from flask import flash, session
# SQLAlchemy imports
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# import database schema for SQLAlchemy
from db_configuration import Base, Category, Item
# import route Blueprints for Flask
from users import user_routes
from apiv1 import apiv1_routes

app = Flask(__name__)
app.register_blueprint(user_routes)
app.register_blueprint(apiv1_routes, url_prefix="/api/v1")
app.secret_key = "LZK82IQ58ICYQA982KOPAXIP"

engine = create_engine("postgres://catalog:newcatalogpassword@localhost/catalog")
Base.metadata.bind = engine
dbSession = sessionmaker(bind=engine)
transaction = dbSession()


@app.route("/", methods=["GET"])
@app.route("/categories", methods=["GET"])
def getCategories():
    """Home route displays all items listed by category"""
    categories = transaction.query(Category).outerjoin("items").all()
    return render_template("categories.html", categories=categories)


@app.route("/categories/<int:catId>/newItem", methods=["GET", "POST"])
def newItem(catId):
    """
    Add a new item to the category
    GET requests display form
    POST requests add item to the database and redirect to item view
    """
    if "user_id" not in session:
        flash("You are not logged in")
        return redirect(url_for("getCategories"))
    if request.method == "POST":
        newItem = Item(name=request.form["name"],
                       description=request.form["description"],
                       cat_id=catId,
                       user_id=session["user_id"])
        transaction.add(newItem)
        transaction.commit()
        flash("Item successfully added")
        return redirect(url_for("viewItem", itemId=newItem.id))
    else:
        category = (transaction.query(Category)
                    .filter(Category.id == catId).one())
        item = Item(id=0, name="", description="", cat_id=category.id)
        return render_template("editItem.html", category=category, item=item)


@app.route("/items/<int:itemId>", methods=["GET"])
def viewItem(itemId):
    """Display all information about a single item"""
    item = (transaction.query(Item).join("category")
            .filter(Item.id == itemId).one())
    return render_template("item.html", item=item)


@app.route("/items/<int:itemId>/edit", methods=["GET", "POST"])
def editItem(itemId):
    """
    Edit an item details
    GET requests display form
    POST requests edit item in the database and redirect to item view
    """
    if "user_id" not in session:
        flash("You are not logged in")
        return redirect(url_for("getCategories"))
    item = (transaction.query(Item).join("category")
            .filter(Item.id == itemId).one())
    if session["user_id"] != item.user_id:
        flash("You cannot edit items that belong to another user")
        return redirect(url_for("getCategories"))
    if request.method == "POST":
        item.name = request.form["name"]
        item.description = request.form["description"]
        item.user_id = session["user_id"]
        transaction.commit()
        flash("Item successfully updated")
        return redirect(url_for("viewItem", itemId=itemId))
    else:
        return render_template("editItem.html",
                               category=item.category, item=item)


@app.route("/items/<int:itemId>/delete", methods=["GET", "POST"])
def deleteItem(itemId):
    """
    Delete an item
    GET requests display confirmation
    POST requests delete the item from the database and redirect to categories
    """
    if "user_id" not in session:
        flash("You are not logged in")
        return redirect(url_for("getCategories"))
    item = (transaction.query(Item).join("category")
            .filter(Item.id == itemId).one())
    if session["user_id"] != item.user_id:
        flash("You cannot delete items that belong to another user")
        return redirect(url_for("getCategories"))
    if request.method == "POST":
        transaction.delete(item)
        transaction.commit()
        flash("Item successfully deleted")
        return redirect(url_for("getCategories"))
    else:
        return render_template("deleteItem.html", item=item)


# Run the application if not being imported
if(__name__ == "__main__"):
    app.debug = True
    app.run(host="0.0.0.0", port=5000)
