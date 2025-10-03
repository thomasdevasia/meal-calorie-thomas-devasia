from fastapi import APIRouter, Depends, HTTPException, status
from app.db.session import get_db
from sqlalchemy.orm import Session
from app.db.models import User
from app.helpers import security
from app.schemas.auth import SignUpData, LoginData
from fastapi_limiter.depends import RateLimiter


router = APIRouter()


@router.post("/auth/signup", status_code=status.HTTP_201_CREATED, dependencies=[Depends(RateLimiter(times=15, seconds=60))])
async def sign_up(data: SignUpData, db: Session = Depends(get_db)):
    if not data.first_name or not data.last_name or not data.email or not data.password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
        )

    try:
        existing_users = db.query(User).filter(User.email == data.email).first()
        if existing_users:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User with this Email already registered",
            )
        hashed_password = security.hash_password(data.password)
        new_user = User(
            first_name=data.first_name,
            last_name=data.last_name,
            email=data.email,
            password_hash=hashed_password,
        )
        db.add(new_user)
        db.commit()
        db.refresh(new_user)

        jwt_token = security.create_access_token(str(new_user.email), str(new_user.id))

        return {"message": "User signed up successfully", "token": jwt_token}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred during sign up",
        )


@router.post("/auth/login", dependencies=[Depends(RateLimiter(times=15, seconds=60))])
async def login(data: LoginData, db: Session = Depends(get_db)):
    try:
        user = db.query(User).filter(User.email == data.email).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="The user does not exist. Please sign up first.",
            )
        if not security.verify_password(data.password, str(user.password_hash)):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid password",
            )
        jwt_token = security.create_access_token(str(user.email), str(user.id))
        return {"message": "User logged in successfully", "token": jwt_token}

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred during login",
        )
