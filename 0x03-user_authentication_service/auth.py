#!/usr/bin/env python3
"""authorization module"""
import bcrypt
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound
from uuid import uuid4
from typing import Union


def _hash_password(password: str) -> bytes:
    """function that hash a string password"""
    ency = password.encode('UTF-8')
    return bcrypt.hashpw(ency, bcrypt.gensalt())


def _generate_uuid() -> str:
    """generate and return UUID"""
    return str(uuid4())


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """method to register a new user"""
        try:
            self._db.find_user_by(email=email)
        except NoResultFound:
            hashed = _hash_password(password)
            new_user = self._db.add_user(email, hashed)
            return new_user
        raise ValueError(f'User {email} already exists')

    def valid_login(self, email: str, password: str) -> bool:
        """method to validate a user by its email and password"""
        try:
            user = self._db.find_user_by(email=email)
            ency = password.encode('utf-8')
            if bcrypt.checkpw(ency, user.hashed_password):
                return True
            return False
        except NoResultFound:
            return False

    def create_session(self, email: str) -> str:
        """create a session and return session_id"""
        try:
            user = self._db.find_user_by(email=email)
            session_id = _generate_uuid()
            self._db.update_user(user.id, session_id=session_id)
            return session_id
        except NoResultFound:
            return None

    def get_user_from_session_id(self, session_id: str) -> Union[User, None]:
        """get user based on session id"""
        if session_id is None:
            return None
        try:
            user = self._db.find_user_by(session_id=session_id)
            return user
        except NoResultFound:
            return None

    def destroy_session(self, user_id: int) -> None:
        """destroy a session based on user id"""
        if user_id:
            self._db.update_user(user_id, session_id=None)
            return
        return None

    def get_reset_password_token(self, email: str) -> str:
        """
        generate a UUID and update the user’s
        reset_token database field. Return the token
        """
        try:
            user = self._db.find_user_by(email=email)
            reset_token = _generate_uuid()
            self._db.update_user(user.id, reset_token=reset_token)
            return reset_token
        except NoResultFound:
            raise ValueError()

    def update_password(self, reset_token: str, password: str) -> None:
        """
        method to update user password
        based on reset_token
        """
        try:
            user = self._db.find_user_by(reset_token=reset_token)
            new_hased_password = _hash_password(password)
            self._db.update_user(
                    user.id,
                    hashed_password=new_hased_password,
                    reset_token=None)
        except NoResultFound:
            raise ValueError()
