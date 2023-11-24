from .models import User
from fastapi import HTTPException, Depends
from typing import Annotated
from .utils import bcrypt_context, ALGORITHM, SECRET_KEY, bearer
from jose import jwt, JWTError
from datetime import datetime, timedelta


def user_authenticate(email: str, password: str, db):
    user = db.query(User).filter(User.email == email).first()

    if not user:
        return False

    check_pass = bcrypt_context.verify(password, user.hashed_password)

    if not check_pass:
        return False

    return user


def create_token(email: str, user_id: str, expirence_time: timedelta):
    encode = {
        "sub": email,
        "id": user_id,
    }

    exp = datetime.now() + expirence_time

    encode.update({"exp": exp})

    return jwt.encode(encode, SECRET_KEY, ALGORITHM)


def get_current_user(token: Annotated[str, bearer]):
    try:
        payloed = jwt.decode(token, SECRET_KEY, ALGORITHM)

        email = payloed.get("sub")
        user_id = payloed.get("id")
        exp = payloed.get("exp")

        if email is None or user_id is None:
            raise HTTPException(status_code=401)

        if datetime.fromtimestamp(exp) < datetime.now():
            raise HTTPException(status_code=401, detail="your token was expired")

        user_info = {"email": email, "user_id": user_id}
        return user_info

    except JWTError:
        return HTTPException("Error")
