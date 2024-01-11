#!/usr/bin/env python3
"""
produces a hashed password
"""
import bcrypt


def hash_password(password: str) -> bytes:
    """
    hashes a password
    """
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    return hashed_password
