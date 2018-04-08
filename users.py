#!/usr/bin/env python3
# Routes for user login and logout

# import Blueprint from Flask library for creating routes
from flask import Blueprint
# import request / response helpers from Flask
from flask import jsonify, render_template, request
# import session helpers from flask
from flask import session as login_session
# import OAuth helpers from oath2client
from oauth2client.client import flow_from_clientsecrets, FlowExchangeError
# SQLAlchemy imports
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
# import core helper libraries
import json, random, requests, string

# import database schema for SQLAlchemy
from db_configuration import Base, User

user_routes = Blueprint("user_routes", __name__)

CLIENT_ID = json.loads(
    open("client_secrets.json", "r").read())["web"]["client_id"]
APPLICATION_NAME = "Sports Catalog"

engine = create_engine("sqlite:///catelog.db")
Base.metadata.bind = engine
dbSession = sessionmaker(bind=engine)
session = dbSession()


@user_routes.route("/login")
def showLogin():
    """Create a state token to prevent request forgery"""
    state = "".join(random.choice(string.ascii_uppercase + string.digits)
                    for x in range(32))
    login_session["state"] = state
    return render_template("login.html", STATE=login_session["state"])


@user_routes.route("/gconnect", methods=["POST"])
def googleConnect():
    # Validate state token
    if request.args.get("state") != login_session["state"]:
        return jsonify("Invalid state parameter."), 401
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
    url = ("https://www.googleapis.com/oauth2/v1/tokeninfo?access_token={}"
           .format(access_token))
    result = requests.get(url).json()
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

    stored_access_token = login_session.get("access_token")
    stored_gplus_id = login_session.get("gplus_id")
    if stored_access_token is not None and gplus_id == stored_gplus_id:
        return jsonify("Current user is already connected."), 200

    # Store the access token in the session for later use.
    login_session["access_token"] = credentials.access_token
    login_session["gplus_id"] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {"access_token": credentials.access_token, "alt": "json"}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    login_session["username"] = data["name"]
    login_session["picture"] = data["picture"]
    login_session["email"] = data["email"]

    output = ""
    output += "<h1>Welcome, "
    output += login_session["username"]
    output += "!</h1>"
    output += '<img src="'
    output += login_session["picture"]
    output += ' " style = "width: 300px; height: 300px;border-radius: 150px;-webkit-border-radius: 150px;-moz-border-radius: 150px;"> '
    # flash("you are now logged in as {}".format(login_session["username"]))
    return output


@user_routes.route("/gdisconnect")
def googleDisconnect():
    """Revoke current user's token and reset their session."""

    # Only disconnect a connected user.
    access_token = login_session["access_token"]
    if access_token is None:
        return jsonify("Current user not connected."), 401

    # Execute HTTP GET request to revoke current token.
    url = "https://accounts.google.com/o/oauth2/revoke?token={}".format(access_token)
    result = requests.get(url)

    if result.status_code == 200:
        # Reset the user's session.
        del login_session["access_token"] 
        del login_session["gplus_id"]
        del login_session["username"]
        del login_session["email"]
        del login_session["picture"]
        return jsonify("Successfully disconnected."), 200
    else:
        # For whatever reason, the given token was invalid.
        return jsonify("Failed to revoke token for given user."), 400
