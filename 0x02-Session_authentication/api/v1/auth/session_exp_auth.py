#!/usr/bin/env python3
"""session authentication expiration"""
from api.v1.auth.session_auth import SessionAuth
from os import getenv
from datetime import datetime, timedelta


class SessionExpAuth(SessionAuth):
    """SessionAuth class with Expiration"""
    def __init__(self):
        """Initialize the class"""
        super().__init__()
        try:
            self.session_duration = int(getenv('SESSION_DURATION', '0'))
        except ValueError:
            self.session_duration = 0

    def create_session(self, user_id=None):
        """create a session for given user id"""
        sess_id = super().create_session(user_id)
        if isinstance(sess_id, str):
            self.user_id_by_session_id[sess_id] = {
                    'user_id': user_id,
                    'created_at': datetime.now()
            }
            return sess_id
        return None

    def user_id_for_session_id(self, session_id=None):
        """gets user id based on session id"""
        if session_id is None:
            return None
        if session_id in self.user_id_by_session_id:
            session_obj = self.user_id_by_session_id[session_id]
            if self.session_duration <= 0:
                return session_obj['user_id']
            if 'created_at' not in session_obj:
                return None
            current_time = datetime.now()
            time_length = timedelta(seconds=self.session_duration)
            exp_time = session_obj['created_at'] + time_length
            if exp_time < current_time:
                return None
            return session_obj['user_id']
