#!/usr/bin/env python3
"""script that creates Auth class"""
from flask import request
from typing import List, TypeVar


class Auth:
    """Auth class"""
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """retrun bool based on the path"""
        if excluded_paths is None or path is None or\
                len(excluded_paths) == 0:
            return True
        endpoint = path.split('/')[3]
        excluded_ep = []
        for i in excluded_paths:
            excluded_ep.append(i.split('/')[3][:-1])
        for i in excluded_ep:
            if i not in endpoint:
                return True
        return False

    def authorization_header(self, request=None) -> str:
        """method that authorize header"""
        if 'Authorization' in request.headers:
            return request.headers.get('Authorization')
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """method return None"""
        return None
