import hashlib

def hash_password(password: str) -> str:
    import bcrypt
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

def verify_password(password: str, hashed: str) -> bool:
    import bcrypt
    return bcrypt.checkpw(password.encode(), hashed.encode())

def require_auth(user):
    if not user or not user.get("is_authenticated"):
        raise PermissionError("Authentication required")
    return True