#!/usr/bin/env python3
"""testing api endpoint module"""
import requests


EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"
BASE_URL = 'http://0.0.0.0:5000'


def register_user(email: str, password: str) -> None:
    """
    function that test a user registration api endpoint
    """
    data = {
        'email': email,
        'password': password
    }
    url = f'{BASE_URL}/users'
    res = requests.post(url, data=data)
    assert res.status_code == 200
    assert res.json() == {'email': 'guillaume@holberton.io',
                          'message': 'user created'}


def log_in_wrong_password(email: str, password: str) -> None:
    """
    function that test a user login with wrong password api endpoint
    """
    data = {
        'email': email,
        'password': password
    }
    url = f'{BASE_URL}/sessions'
    res = requests.post(url, data=data)
    assert res.status_code == 401


def log_in(email: str, password: str) -> str:
    """
    function that test a user login api endpoint
    """
    data = {
        'email': email,
        'password': password
    }
    url = f'{BASE_URL}/sessions'
    res = requests.post(url, data=data)
    assert res.status_code == 200
    assert res.json() == {"email": f'{email}', "message": "logged in"}
    return res.cookies.get('session_id')


def profile_unlogged() -> None:
    """
    function that test unlogged user profile api endpoint
    """
    url = f'{BASE_URL}/profile'
    res = requests.get(url)
    assert res.status_code == 403


def profile_logged(session_id: str) -> None:
    """
    function that test logged user profile api endpoint
    """
    cookies = {'session_id': session_id, }
    url = f'{BASE_URL}/profile'
    res = requests.get(url, cookies=cookies)
    assert res.status_code == 200
    email = res.json()['email']
    assert res.json() == {"email": f'{email}'}


def log_out(session_id: str) -> None:
    """
    function that test a user logout api endpoint
    """
    cookies = {'session_id': session_id, }
    url = f'{BASE_URL}/sessions'
    res = requests.delete(url, cookies=cookies)
    assert res.status_code == 200
    assert res.json() == {"message": "Bienvenue"}


def reset_password_token(email: str) -> str:
    """
    function that test a reset password token api endpoint
    """
    data = {'email': email}
    url = f'{BASE_URL}/reset_password'
    res = requests.post(url, data=data)
    assert res.status_code == 200
    reset_token = res.json()['reset_token']
    assert res.json() == {"email": f'{email}', "reset_token": f'{reset_token}'}
    return reset_token


def update_password(email: str, reset_token: str, new_password: str) -> None:
    """
    function that test an update password api endpoint
    """
    data = {
        'email': email,
        'reset_token': reset_token,
        'new_password': new_password
    }
    url = f'{BASE_URL}/reset_password'
    res = requests.put(url, data=data)
    assert res.status_code == 200
    assert res.json() == {"email": f'{email}', "message": "Password updated"}


if __name__ == "__main__":

    register_user(EMAIL, PASSWD)
    log_in_wrong_password(EMAIL, NEW_PASSWD)
    profile_unlogged()
    session_id = log_in(EMAIL, PASSWD)
    profile_logged(session_id)
    log_out(session_id)
    reset_token = reset_password_token(EMAIL)
    update_password(EMAIL, reset_token, NEW_PASSWD)
    log_in(EMAIL, NEW_PASSWD)
