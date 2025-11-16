import os
import sys

import pytest

ROOT_DIR = os.path.dirname(os.path.dirname(__file__))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from core import operations
from core.security import hash_password_or_token


def test_login_user_success(monkeypatch):
    password = 'correct_password'
    stored_hash = hash_password_or_token(password)
    users_data = {
        'users': [
            {
                'id': 'user-123',
                'email': 'user@example.com',
                'pwd_hash': stored_hash,
                'is_active': True,
            }
        ]
    }

    sessions_data = {'sessions': []}

    monkeypatch.setattr(operations, 'read_json', lambda: users_data)
    monkeypatch.setattr(operations, 'read_sessions', lambda: sessions_data)
    monkeypatch.setattr(operations, 'write_sessions', lambda data: None)
    monkeypatch.setattr(operations, 'make_token', lambda: 'fixed-token')

    result = operations.login_user('user@example.com', password)

    assert result == {'user_id': 'user-123', 'session_token': 'fixed-token'}
