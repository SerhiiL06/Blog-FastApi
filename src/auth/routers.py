from fastapi import APIRouter, Depends, HTTPException, Response
from typing import Annotated
from fastapi.security import OAuth2PasswordRequestForm
from core.database import SessionLocal, get_db
from .utils import bcrypt_context
from .models import User
from .logic import user_authenticate, create_token, get_current_user
from .schemes import UserCreateScheme, UserReadScheme, ChangePasswordScheme
from datetime import timedelta


auth_router = APIRouter(prefix="/auth", tags=["auth"])


@auth_router.post("/register", response_model=UserReadScheme)
async def register_user(
    user_info: UserCreateScheme, db: SessionLocal = Depends(get_db)
):
    new_user = User(
        email=user_info.email,
        first_name=user_info.first_name.capitalize(),
        last_name=user_info.last_name.capitalize(),
        hashed_password=bcrypt_context.hash(user_info.password),
    )

    db.add(new_user)
    db.commit()

    return new_user


@auth_router.post("/login")
async def login_user(
    user_request: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: SessionLocal = Depends(get_db),
):
    user = user_authenticate(user_request.username, user_request.password, db)

    if not user:
        return HTTPException(
            status_code=401, detail="Email or password was not correct"
        )

    token = create_token(
        email=user.email,
        user_id=user.id,
        expirence_time=timedelta(minutes=30),
    )
    return token


@auth_router.get("/user-list", response_model=list[UserReadScheme])
async def user_list(db: SessionLocal = Depends(get_db)):
    return db.query(User).all()


@auth_router.get("/users/me", response_model=UserReadScheme)
async def get_profile(
    user: dict = Depends(get_current_user),
    db: SessionLocal = Depends(get_db),
):
    user_info = db.query(User).filter(User.email == user.get("email")).first()

    if not user_info:
        return HTTPException("Auth info don't providet")

    return user_info


@auth_router.patch("/change-password")
async def change_password(
    password: ChangePasswordScheme,
    user_request: dict = Depends(get_current_user),
    db: SessionLocal = Depends(get_db),
):
    if not user_request:
        return HTTPException(detail="Token was not providet", status_code=401)

    user = db.query(User).filter(User.id == user_request.get("user_id")).first()

    if not bcrypt_context.verify(password.old_password, user.hashed_password):
        return HTTPException(status_code=402, detail="Your current password incorrect")

    user.hashed_password = bcrypt_context.hash(password.new_password)

    db.commit()

    return Response("Password update")
