from fastapi import APIRouter, Depends, HTTPException, Response
from typing import Annotated
from fastapi.security import OAuth2PasswordRequestForm

from core.database import SessionLocal, database_dependens
from .utils import current_user
from config import bcrypt_context
from .models import User
from .logic import user_authenticate, create_token, create_or_update_user
from .schemes import UserCreateScheme, UserReadScheme, UserScheme, ChangePasswordScheme
from datetime import timedelta


auth_router = APIRouter(prefix="/auth", tags=["auth"])


@auth_router.post("/register", response_model=UserReadScheme)
async def register_user(user_info: UserCreateScheme, db: database_dependens):
    new_user = create_or_update_user(new_info=user_info, created=False)

    db.add(new_user)
    db.commit()

    return new_user


@auth_router.post("/login")
async def login_user(
    user_request: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: database_dependens,
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
async def user_list(db: database_dependens):
    return db.query(User).all()


@auth_router.get("/users/me", response_model=UserReadScheme)
async def get_profile(
    user: current_user,
    db: database_dependens,
):
    user_info = db.query(User).filter(User.email == user.get("email")).first()

    if not user_info:
        return HTTPException("Auth info don't providet")

    return user_info


@auth_router.patch("/update-profile", response_model=UserReadScheme)
async def update_me(
    user: current_user, update_info: UserScheme, db: database_dependens
):
    user = db.query(User).get(user.get("user_id"))

    if user is None:
        raise HTTPException(status_code=401, detail="You must be authorizate")

    create_or_update_user(old_info=user, new_info=update_info)

    db.commit()

    return user


@auth_router.patch("/change-password")
async def change_password(
    password: ChangePasswordScheme,
    user_request: current_user,
    db: database_dependens,
):
    if not user_request:
        return HTTPException(detail="Token was not providet", status_code=401)

    user = db.query(User).filter(User.id == user_request.get("user_id")).first()

    if not bcrypt_context.verify(password.old_password, user.hashed_password):
        return HTTPException(status_code=402, detail="Your current password incorrect")

    user.hashed_password = bcrypt_context.hash(password.new_password)

    db.commit()

    return Response("Password update")
