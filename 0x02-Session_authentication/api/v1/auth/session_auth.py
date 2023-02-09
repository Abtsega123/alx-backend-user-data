#!/usr/bin/env python3
"""Session authentication"""
from api.v1.auth.auth import Auth
from uuid import uuid4
from models.user import User


class SessionAuth(Auth):
    """creates SessionAuth calss"""
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """creates a Session ID for a user_id"""
        if user_id is None or not isinstance(user_id, str):
            return None
        uid = str(uuid4())
        SessionAuth.user_id_by_session_id[uid] = user_id
        return uid

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """returns a User ID based on a Session ID"""
        if session_id is None or not isinstance(session_id, str):
            return None
        return SessionAuth.user_id_by_session_id.get(session_id)

    def current_user(self, request=None):
        """hat returns a User instance based on a cookie value"""
        cookie_value = self.session_cookie(request)
        user_id = SessionAuth.user_id_by_session_id.get(cookie_value)
        return User.get(user_id)

    def destroy_session(self, request=None):
        """deletes the user session / logout"""
        if request is None:
            return False
        if self.session_cookie(request):
            cookie = self.session_cookie(request)
            if SessionAuth.user_id_by_session_id.get(cookie):
                del SessionAuth.user_id_by_session_id[cookie]
                return True
            return False
        return False
