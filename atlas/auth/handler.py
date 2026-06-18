import os
from datetime import datetime, timedelta
import jwt
from passlib.context import CryptContext

class AuthHandler:
    """Handles JWT generation and password hashing for Atlas using PyJWT."""

    SECRET_KEY = os.getenv("ATLAS_SECRET_KEY", "super-secret-atlas-key")
    ALGORITHM = "HS256"
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    @classmethod
    def verify_password(cls, plain_password, hashed_password):
        return cls.pwd_context.verify(plain_password, hashed_password)

    @classmethod
    def get_password_hash(cls, password):
        return cls.pwd_context.hash(password)

    @classmethod
    def create_access_token(cls, data: dict, expires_delta: timedelta = None):
        to_encode = data.copy()
        expire = datetime.utcnow() + (expires_delta or timedelta(minutes=15))
        to_encode.update({"exp": expire})
        return jwt.encode(to_encode, cls.SECRET_KEY, algorithm=cls.ALGORITHM)
