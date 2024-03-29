#!/usr/bin/env python3
"""
auth module
"""
import bcrypt
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound
import uuid
from flask import Flask, jsonify, request, redirect


def _hash_password(password: str) -> bytes:
    """
    hashes a password
    """
    salted = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salted)

    return hashed


def _generate_uuid() -> str:
    """
    generates a uuid
    """
    return str(uuid.uuid4())


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """
        registers a new user
        """
        try:
            existing_user = self._db.find_user_by(email=email)
            raise ValueError(f"User {existing_user.email} already exists")
        except NoResultFound:
            pass
        hashed_password = _hash_password(password)
        new_user = self._db.add_user(email=email,
                                     hashed_password=hashed_password)
        return new_user

    def valid_login(self, email: str, password: str) -> bool:
        """
        validates user credentials
        """
        try:
            user = self._db.find_user_by(email=email)
            return bcrypt.checkpw(password.encode('utf-8'),
                                  user.hashed_password)
        except NoResultFound:
            return False

    def create_session(self, email: str) -> str:
        """
        creates new session for user
        """
        try:
            user = self._db.find_user_by(email=email)
            session_id = _generate_uuid()
            self._db._session.query(User).filter_by(email=email)\
                .update({"session_id": session_id})
            self._db._session.commit()
            return session_id
        except NoResultFound:
            return None

    def get_user_from_session_id(self, session_id: str) -> User:
        """
        finds user from session id
        """
        try:
            return self._db.find_user_by(session_id=session_id)
        except NoResultFound:
            return None

    def destroy_session(self, user_id: int) -> None:
        """
        destroys session
        """
        try:
            user = self._db.find_user_by(id=user_id)
            user.session_id = None
            self._db._session.commit()
        except NoResultFound:
            return None

    def get_reset_password_token(self, email: str) -> str:
        """
        get reset password token
        """
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            raise ValueError(f"User with email {email} not found")
        reset_token = str(uuid.uuid4())
        user.reset_token = reset_token
        self._db._session.commit()
        return reset_token

    def update_password(self, reset_token: str, password: str) -> None:
        """
        updates password
        """
        user = self._db.find_user_by(reset_token=reset_token)
        user.hashed_password = _hash_password(password)
        user.reset_token = None
        self._db._session.commit()
