#!/usr/bin/env python3
# Routes for user login and logout

# import Blueprint from Flask library for creating routes
from flask import Blueprint
# import request / response helpers from Flask
from flask import flash, jsonify, render_template, request
from flask import abort, redirect, url_for
# import session helpers from flask
from flask import session
# import OAuth helpers from oath2client
from oauth2client.client import flow_from_clientsecrets, FlowExchangeError
# SQLAlchemy imports
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
# import core helper libraries
import json
import random
import requests
import string

# import database schema for SQLAlchemy
from db_configuration import Base, User

user_routes = Blueprint("user_routes", __name__)

CLIENT_ID = json.loads(
    open("client_secrets.json", "r").read())["web"]["client_id"]
APPLICATION_NAME = "Sports Catalog"

engine = create_engine("sqlite:///catelog.db")
Base.metadata.bind = engine
dbSession = sessionmaker(bind=engine)
transaction = dbSession()


# User helper functions
def createUser(user_info):
    """Add new user to the database and return the new user id"""
    newUser = User(name=user_info["username"], email=user_info["email"])
    transaction.add(newUser)
    transaction.commit()
    user = transaction.query(User).filter_by(email=user_info["email"]).one()
    return user.id


def getUserInfo(user_id):
    """Get user information based on user_id"""
    user = transaction.query(User).filter_by(id=user_id).one()
    return user


def getUserID(email):
    """Get user id based on email address"""
    user = transaction.query(User).filter_by(email=email).first()
    if user is None:
        return None
    return user.id


@user_routes.before_request
def checkState():
    """Add state to session to prevent csrf"""
    if "state" not in session:
        s = "".join(random.choice(string.ascii_uppercase + string.digits)
                    for x in range(32))
        session["state"] = s
    # verify CSRF state token on post requests
    if request.method == "POST":
        if (session["state"] != request.form.get("state")
            and session["state"] != request.args.get("state")):
            abort(400)


@user_routes.route("/gconnect", methods=["POST"])
def googleConnect():
    """Connect to Google account token"""
    # Obtain authorization code
    code = request.data

    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets("client_secrets.json", scope="")
        oauth_flow.redirect_uri = "postmessage"
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        return jsonify("Failed to upgrade the authorization code."), 401

    # Check that the access token is valid.
    access_token = credentials.access_token
    url = "https://www.googleapis.com/oauth2/v1/tokeninfo?access_token={}"
    result = requests.get(url.format(access_token)).json()
    # If there was an error in the access token info, abort.
    if result.get("error") is not None:
        return jsonify(result.get("error")), 500

    # Verify that the access token is used for the intended user.
    gplus_id = credentials.id_token["sub"]
    if result["user_id"] != gplus_id:
        return jsonify("Token's user ID doesn't match given user ID."), 401

    # Verify that the access token is valid for this app.
    if result["issued_to"] != CLIENT_ID:
        return jsonify("Token's client ID does not match app's."), 401

    stored_access_token = session.get("access_token")
    stored_gplus_id = session.get("gplus_id")
    if stored_access_token is not None and gplus_id == stored_gplus_id:
        return jsonify("Current user is already connected."), 200

    # Store the access token in the session for later use.
    session["access_token"] = credentials.access_token
    session["gplus_id"] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {"access_token": credentials.access_token, "alt": "json"}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    session["username"] = data["name"]
    session["email"] = data["email"]

    # see if user exists, if it doesn't make a new one
    user_id = getUserID(session["email"])
    if not user_id:
        user_id = createUser(session)
    session["user_id"] = user_id

    flash("Logged in as {}".format(session["username"]))
    return jsonify("Login Success"), 200


@user_routes.route("/gdisconnect")
def googleDisconnect():
    """Revoke current user's token and reset their session."""
    # Only disconnect a connected user.
    access_token = session.get("access_token", None)
    if access_token is None:
        return jsonify("Current user not connected."), 401

    # Execute HTTP GET request to revoke current token.
    url = "https://accounts.google.com/o/oauth2/revoke?token={}"
    result = requests.get(url.format(access_token))

    if result.status_code == 200:
        # Reset the user's session.
        del session["user_id"]
        del session["access_token"]
        del session["gplus_id"]
        del session["username"]
        del session["email"]
        flash("You have successfully logged out")
        return redirect(url_for("getCategories"))
    else:
        # For whatever reason, the given token was invalid.
        flash("Unable to log out")
        return jsonify("Failed to revoke token for given user."), 400

# prevent file from attempting to run alone
if(__name__ == "__main__"):
    print("This file cannot be run directly")
