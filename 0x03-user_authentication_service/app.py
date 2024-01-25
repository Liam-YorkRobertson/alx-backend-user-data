#!/usr/bin/env python3
"""
basic flask app
"""
from flask import Flask, jsonify, request
from auth import Auth


AUTH = Auth()
app = Flask(__name__)


@app.route("/")
def index():
    """
    returns message
    """
    return jsonify({"message": "Bienvenue"})


@app.route("/users", methods=["POST"])
def register_user():
    """
    register new user
    """
    try:
        email = request.form.get("email")
        password = request.form.get("password")
        user = AUTH.register_user(email, password)
        return jsonify({"email": user.email, "message": "user created"})
    except ValueError as error:
        return jsonify({"message": str(error)}), 400


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
