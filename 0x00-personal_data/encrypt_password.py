#!/usr/bin/env python3
"""script that encripts passwords"""
import bcrypt


def hash_password(password: str) -> bytes:
    """function that hash a password"""
    hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
    return hashed


def is_valid(hashed_password: bytes, password: str) -> bool:
    """checks if the hash password is formed from the given password"""
    if bcrypt.checkpw(password.encode(), hashed_password):
        return True
    return False
