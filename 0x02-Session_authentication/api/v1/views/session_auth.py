#!/usr/bin/env python3
""" handles all routes for the Session authentication"""
from api.v1.views import app_views
from flask import jsonify, request, make_response
from models.user import User
from os import getenv


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def sess_login():
    """function to allow user to login in"""
    email = request.form.get('email')
    if not email:
        return jsonify({"error": "email missing"}), 400
    password = request.form.get('password')
    if not password:
        return jsonify({"error": "password missing"}), 400
    users = User.search()
    try:
        curr_user = [user for user in users if user.email == email]
        user = curr_user[0]
        if user.is_valid_password(password):
            from api.v1.app import auth
            session_id = auth.create_session(user.id)
            res = make_response(jsonify(user.to_json()))
            res.set_cookie(getenv('SESSION_NAME'), session_id)
            return res
        else:
            return jsonify({"error": "wrong password"}), 401
    except IndexError:
        return jsonify({"error": "no user found for this email"}), 404


@app_views.route('/auth_session/logout',
                 methods=['DELETE'], strict_slashes=False)
def delete_session():
    """function to delete user session"""
    from api.v1.app import auth
    if auth.destroy_session(request):
        return jsonify({}), 200
    abort(404)
