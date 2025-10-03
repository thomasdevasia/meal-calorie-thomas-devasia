from fastapi.security import OAuth2PasswordBearer
from app.helpers import security
from fastapi import Depends, HTTPException, status

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail={"detail": "Could not validate credentials. Try logging in again."},
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        jwt = security.verify_access_token(token)
    except Exception:
        raise credentials_exception
    
    return jwt