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
