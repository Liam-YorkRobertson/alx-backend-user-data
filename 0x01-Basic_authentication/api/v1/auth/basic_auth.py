#!/usr/bin/env python3
"""
manages basic authorisation
"""
from .auth import Auth


class BasicAuth(Auth):
    """
    basic auth class
    """
    def extract_base64_authorization_header(self, auth_header: str) -> str:
        """
        get base64 from auth header
        """
        if auth_header is None or not isinstance(auth_header, str):
            return None
        if not auth_header.startswith('Basic '):
            return None
        base64_part = auth_header.split('Basic ')[1].strip()
        return base64_part