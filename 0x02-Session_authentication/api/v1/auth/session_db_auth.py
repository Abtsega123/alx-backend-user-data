#!/usr/bin/env python3
"""Session authentication Database"""
from api.v1.auth.session_exp_auth import SessionExpAuth
from datetime import datetime, timedelta
from models.user_session import UserSession


class SessionDBAuth(SessionExpAuth):
    """Session database Class"""
    def create_session(self, user_id=None):
        """
        creates and stores new instance of
        UserSession and returns the Session ID
        """
        session_id = super().create_session(user_id)
        if session_id is not None:
            kwargs = {'user_id': user_id, 'session_id': session_id}
            user_session = UserSession(**kwargs)
            user_session.save()
            return session_id

    def user_id_for_session_id(self, session_id=None):
        """
        eturns the User ID by requesting UserSession
        in the database based on session_id
        """
        try:
            sessions = UserSession.search({'session_id': session_id})
        except Exception:
            return None
        if len(sessions) > 0:
            current_time = datetime.now()
            time_length = timedelta(seconds=self.session_duration)
            exp_time = sessions[0].created_at + time_length
            if exp_time < current_time:
                return None
            return sessions[0].user_id
        return None

    def destroy_session(self, request=None):
        """
        destroys the UserSession based on the
        Session ID from the request cookie
        """
        try:
            sessions = UserSession.search({'session_id': session_id})
        except Exception:
            return False
        if len(sessions) > 0:
            sessions[0].remove()
            return True
        return False
