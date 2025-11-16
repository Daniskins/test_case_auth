import hashlib
import secrets
from hmac import compare_digest
import uuid

def hash_password_or_token(text: str) -> str:
    obj = hashlib.sha3_256()
    obj.update(text.encode('utf-8'))
    return obj.hexdigest()

def verify_password(curr_hash_pwd: str, other_hash_pwd: str) -> bool:
    return compare_digest(curr_hash_pwd, other_hash_pwd)

def make_token() -> str:
    return secrets.token_urlsafe(64)

def generate_id() -> str:
    key = uuid.uuid1()
    return str(key)
