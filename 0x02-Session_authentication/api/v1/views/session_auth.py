#!/usr/bin/env python3
"""
manages session auth view
"""
from flask import jsonify, request
from api.v1.views import app_views
from models.user import User


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def login():
    """
    user login
    """
    email = request.form.get('email')
    password = request.form.get('password')
    if not email or not password:
        return jsonify({"error": "email or password missing"}), 400
    users = User.search({'email': email})
    if not users:
        return jsonify({"error": "no user found for this email"}), 404
    user = users[0]
    if not user.is_valid_password(password):
        return jsonify({"error": "wrong password"}), 401
    from api.v1.app import auth
    session_id = auth.create_session(user.id)
    user_data = user.to_json()
    response = jsonify(user_data)
    response.set_cookie(auth.session_name, session_id)
    return response
