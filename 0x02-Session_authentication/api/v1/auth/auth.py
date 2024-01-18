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
        return (
            path is not None
            and excluded_paths is not None
            and not any(
                path.startswith(excluded[:-1])
                if excluded.endswith("*") else path == excluded
                for excluded in excluded_paths
            )
        )

    def authorization_header(self, request=None) -> str:
        """
        get auth header
        """
        if request is None or 'Authorization' not in request.headers:
            return None
        return request.headers['Authorization']

    def current_user(self, request=None) -> TypeVar('User'):
        """
        get current user
        """
        return None
