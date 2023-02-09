#!/usr/bin/env python3
"""basic authentication"""
from api.v1.auth.auth import Auth
import base64
from typing import TypeVar
from models.user import User


class BasicAuth(Auth):
    """creates BasicAuth class"""
    def extract_base64_authorization_header(
            self, authorization_header: str) -> str:
        """
        returns the Base64 part of the Authorization
        header for a Basic Authentication
        """
        if authorization_header is None or\
                not isinstance(authorization_header, str) or\
                authorization_header[:6] != "Basic ":
            return None
        return authorization_header[6:]

    def decode_base64_authorization_header(
            self, base64_authorization_header: str) -> str:
        """
        returns the decoded value of a Base64
        string base64_authorization_header
        """
        if base64_authorization_header is None or\
                not isinstance(base64_authorization_header, str):
            return None
        try:
            _64 = base64_authorization_header.encode('utf-8')
            decoded = base64.b64decode(_64)
            return decoded.decode('utf-8')
        except Exception:
            return None

    def extract_user_credentials(
            self, decoded_base64_authorization_header: str) -> (str, str):
        """
        returns the user email and password
        from the Base64 decoded value
        """
        if decoded_base64_authorization_header is None or\
                not isinstance(decoded_base64_authorization_header, str) or\
                ':' not in decoded_base64_authorization_header:
            return (None, None)
        credentials = decoded_base64_authorization_header.split(':')
        user = credentials[0]
        password = ':'.join(credentials[1:])
        return (f'{user}', f'{password}')

    def user_object_from_credentials(
            self, user_email: str, user_pwd: str) -> TypeVar('User'):
        """returns the User instance based on his email and password"""
        if user_email is None or not isinstance(user_email, str) or\
                user_pwd is None or not isinstance(user_pwd, str):
            return None
        try:
            users = User.search()
        except Exception:
            return None
        if len(users):
            for user in users:
                if user.email == user_email:
                    if user.is_valid_password(user_pwd):
                        return user
            return None
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """
        method that overloads Auth and retrieves
        the User instance for a request
        """
        auth_header = self.authorization_header(request)
        if auth_header:
            base64_auth = self.extract_base64_authorization_header(auth_header)
            decode_auth = self.decode_base64_authorization_header(base64_auth)
            email, password = self.extract_user_credentials(decode_auth)
            return self.user_object_from_credentials(email, password)
