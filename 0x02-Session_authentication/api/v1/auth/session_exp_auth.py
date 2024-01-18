#!/usr/bin/env python3
"""
manages session expiration auth
"""
from api.v1.auth.session_auth import SessionAuth
from datetime import datetime, timedelta
import os


class SessionExpAuth(SessionAuth):
    """
    session exp auth class
    """
    def __init__(self):
        """
        initialization
        """
        try:
            time = int(os.getenv('SESSION_DURATION'))
        except Exception:
            time = 0
        self.session_duration = time

    def create_session(self, user_id=None):
        """
        creates session with exp
        """
        session_id = super().create_session(user_id)
        if session_id is None:
            return None
        self.user_id_by_session_id[session_id] = {
            'user_id': user_id,
            'created_at': datetime.now()
        }
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """
        returns user id based on session id with exp
        """
        if session_id is None or session_id not in self.user_id_by_session_id:
            return None
        session_dict = self.user_id_by_session_id[session_id]
        if self.session_duration <= 0:
            return session_dict['user_id']
        if 'created_at' not in session_dict:
            return None
        created_at = session_dict['created_at']
        expiration_time = created_at + timedelta(seconds=self.session_duration)
        if datetime.now() > expiration_time:
            return None
        return session_dict['user_id']
