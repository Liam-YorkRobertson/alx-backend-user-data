#!/usr/bin/env python3
"""
manages basic authorisation
"""
from .auth import Auth
import base64
from models.user import User


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

    def extract_user_credentials(self, decoded_base64_auth_header:
                                 str) -> (str, str):
        """
        get user data from auth header
        """
        if not decoded_base64_auth_header or not isinstance(
                decoded_base64_auth_header, str):
            return None, None
        if ':' not in decoded_base64_auth_header:
            return None, None
        user_email, user_password = decoded_base64_auth_header.split(':', 1)
        return user_email, user_password

    def user_object_from_credentials(self, user_email: str,
                                     user_pwd: str) -> User:
        """
        get user instance
        """
        if not user_email or not isinstance(user_email, str):
            return None
        if not user_pwd or not isinstance(user_pwd, str):
            return None
        users = User.search({"email": user_email})
        if not users:
            return None
        for user in users:
            if user.is_valid_password(user_pwd):
                return user
        return None

    def current_user(self, request=None) -> User:
        """
        get user based on auth
        """
        if request is None:
            return None
        auth_header = self.authorization_header(request)
        base64_header = self.extract_base64_authorization_header(auth_header)
        decoded_header = self.decode_base64_authorization_header(base64_header)
        email, pwd = self.extract_user_credentials(decoded_header)
        user = self.user_object_from_credentials(email, pwd)
        return user
