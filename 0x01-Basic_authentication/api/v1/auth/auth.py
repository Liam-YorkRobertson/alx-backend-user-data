#!/usr/bin/env python3
"""
manages API authentication
"""
from flask import request
from typing import List, TypeVar


class Auth:
    """
    authorisation class
    """
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
        check if path requires auth
        """
        return False

    def authorization_header(self, request=None) -> str:
        """
        get auth header
        """
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """
        get current user
        """
        return None
