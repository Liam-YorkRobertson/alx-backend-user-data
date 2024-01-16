#!/usr/bin/env python3
"""
manages basic authorisation
"""
from .auth import Auth
import base64


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

    def decode_base64_authorization_header(self,
                                           base64_auth_header: str) -> str:
        """
        decode base64 auth header
        """
        if base64_auth_header is None or not isinstance(base64_auth_header,
                                                        str):
            return None
        try:
            decode_bytes = base64.b64decode(base64_auth_header)
            decode_str = decode_bytes.decode('utf-8')
            return decode_str
        except (UnicodeDecodeError, base64.binascii.Error):
            return None

    def extract_user_credentials(self, decoded_base64_auth_header: str) -> (str, str):
        """
        get user data from auth header
        """
        if not decoded_base64_auth_header or not isinstance(decoded_base64_auth_header, str):
            return None, None
        if ':' not in decoded_base64_auth_header:
            return None, None
        user_email, user_password = decoded_base64_auth_header.split(':', 1)
        return user_email, user_password
