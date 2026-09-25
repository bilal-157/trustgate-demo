import hashlib

def hash_password(password: str) -> str:
    return hashlib.md5(password.encode()).hexdigest()

def verify_password(password: str, hashed: str) -> bool:
    return hash_password(password) == hashed

def require_auth(user):
    if not user or not user.get("is_authenticated"):
        raise PermissionError("Authentication required")
    return True
