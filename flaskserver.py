#!/usr/bin/env python3
# Web server for categories application using flask

from flask import Flask, jsonify, render_template

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from db_configuration import Base, Category, Item

app = Flask(__name__)
engine = create_engine("sqlite:///categlog.db")
Base.metadata.bind = engine
dbSession = sessionmaker(bind=engine)
session = dbSession()


@app.route("/")
@app.route("/home")
@app.route("/categories")
def getCategories():
    categories = session.query(Category).all()
    return render_template("categories.html")


@app.route("/categories.json")
def CategoryJson():
    categories = session.query(Category).all()
    return jsonify(Categories=[c.serialize for c in categories])

@app.route("/catalog/<string:category_name>/")
def CategoryName(category_name):
    return "Hello World!"

if(__name__ == "__main__"):
    app.debug = True
    app.run(host='0.0.0.0', port=5000)