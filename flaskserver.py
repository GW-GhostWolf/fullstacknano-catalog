#!/usr/bin/env python3
# Web server for categories application using Flask (http://flask.pocoo.org/)
# and SQLAlchemy (http://www.sqlalchemy.org/)

# import main Flask library
from flask import Flask
# import request / response helpers from Flask
from flask import jsonify, redirect, render_template, request, url_for
# import session helpser from flask
from flask import session
# SQLAlchemy imports
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# import database schema for SQLAlchemy
from db_configuration import Base, Category, Item
# import route Blueprints for Flask
from users import user_routes

app = Flask(__name__)
app.register_blueprint(user_routes)

engine = create_engine("sqlite:///catelog.db")
Base.metadata.bind = engine
dbSession = sessionmaker(bind=engine)
transaction = dbSession()


@app.route("/", methods=["GET"])
@app.route("/categories", methods=["GET"])
def getCategories():
    """Home route displays all items listed by category"""
    categories = transaction.query(Category).outerjoin("items").all()
    return render_template("categories.html", categories=categories)


@app.route("/category/<int:catId>/newItem", methods=["GET", "POST"])
def newItem(catId):
    """
    Add a new item to the category
    GET requests display form
    POST requests add item to the database and redirect to item view
    """
    if "username" not in session:
        return redirect(url_for("user_routes.showLogin"))
    if request.method == "POST":
        newItem = Item(name=request.form["name"],
                       description=request.form["description"],
                       cat_id=catId)
        transaction.add(newItem)
        transaction.commit()
        return redirect(url_for("viewItem", itemId=newItem.id))
    else:
        category = (transaction.query(Category)
                    .filter(Category.id == catId).one())
        item = Item(id=0, name="", description="", cat_id=category.id)
        return render_template("editItem.html", category=category, item=item)


@app.route("/item/<int:itemId>", methods=["GET"])
def viewItem(itemId):
    """Display all information about a single item"""
    item = (transaction.query(Item).join("category")
            .filter(Item.id == itemId).one())
    return render_template("item.html", item=item)


@app.route("/item/<int:itemId>/edit", methods=["GET", "POST"])
def editItem(itemId):
    """
    Edit an item details
    GET requests display form
    POST requests edit item in the database and redirect to item view
    """
    if "username" not in session:
        return redirect(url_for("user_routes.showLogin"))
    item = (transaction.query(Item).join("category")
            .filter(Item.id == itemId).one())
    if request.method == "POST":
        item.name = request.form["name"]
        item.description = request.form["description"]
        transaction.commit()
        return redirect(url_for("viewItem", itemId=itemId))
    else:
        return render_template("editItem.html",
                               category=item.category, item=item)


@app.route("/item/<int:itemId>/delete", methods=["GET", "POST"])
def deleteItem(itemId):
    """
    Delete an item
    GET requests display confirmation
    POST requests delete the item from the database and redirect to categories
    """
    if "username" not in session:
        return redirect(url_for("user_routes.showLogin"))
    item = (transaction.query(Item).join("category")
            .filter(Item.id == itemId).one())
    if request.method == "POST":
        transaction.delete(item)
        transaction.commit()
        return redirect(url_for("getCategories"))
    else:
        return render_template("deleteItem.html", item=item)


@app.route("/categories.json", methods=["GET"])
def CategoryJson():
    categories = transaction.query(Category).join("items").all()
    return jsonify(Categories=[c.serializable for c in categories])


# Run the application if not being imported
if(__name__ == "__main__"):
    app.secret_key = "LZK82IQ58ICYQA982KOPA"
    app.debug = True
    app.run(host="0.0.0.0", port=5000)
