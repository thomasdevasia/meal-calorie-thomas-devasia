from app.config import Settings
from jose import jwt, JWTError
import bcrypt
from datetime import datetime, timedelta, timezone

settings = Settings()

def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))

def create_access_token(email: str, user_id: str) -> str:
    expire = datetime.now(timezone.utc) + timedelta(minutes=settings.jwt_expire_minutes)
    to_encode = {"email": email, "exp": expire, "user_id": user_id}
    encoded_jwt = jwt.encode(to_encode, settings.jwt_secret, algorithm=settings.jwt_algo)
    return encoded_jwt

def verify_access_token(token: str) -> dict:
    try:
        payload = jwt.decode(token, settings.jwt_secret, algorithms=[settings.jwt_algo])
        email = payload.get("email")
        if not isinstance(email, str):
            raise JWTError
        if not payload.get("user_id"):
            raise JWTError
        return payload
    except JWTError:
        raise JWTError("Could not validate credentials. Try logging in again.")