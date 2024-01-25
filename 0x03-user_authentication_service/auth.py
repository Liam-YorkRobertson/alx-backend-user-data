#!/usr/bin/env python3
"""
auth module
"""
import bcrypt


def _hash_password(password: str) -> bytes:
    """
    hashes a password
    """
    salted = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salted)

    return hashed
