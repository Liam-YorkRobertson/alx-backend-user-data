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


def is_valid(hashed_password: bytes, password: str) -> bool:
    """
    validates a hashed password
    """
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password)
