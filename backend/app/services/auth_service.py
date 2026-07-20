from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from backend.app.core.security import hash_password
from backend.app.models.user import User
from backend.app.schemas.auth import UserRegister

from backend.app.core.jwt import create_access_token
from backend.app.core.security import verify_password
from backend.app.schemas.auth import UserLogin, TokenResponse


class AuthService:

    @staticmethod
    def register_user(db: Session, user_data: UserRegister) -> User:

        existing_user = db.scalar(
            select(User).where(User.email == user_data.email)
        )

        if existing_user:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email already registered")

        existing_username = db.scalar(
            select(User).where(User.username == user_data.username)
        )

        if existing_username:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Username already exists")

        user = User(
            username=user_data.username,
            email=user_data.email,
            password_hash=hash_password(user_data.password),
            role="patient",
        )

        db.add(user)
        db.commit()
        db.refresh(user)

        return user
    

    @staticmethod
    def login_user(db: Session, credentials: UserLogin) -> TokenResponse:

        user = db.scalar(
            select(User).where(User.email == credentials.email)
        )

        if user is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password")

        if not verify_password(
            credentials.password,
            user.password_hash,
        ):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password")

        access_token = create_access_token(
            {
                "sub": str(user.id),
                "email": user.email,
            }
        )

        return TokenResponse(
            access_token=access_token
        )
