from .models import User
from fastapi import HTTPException

from config import bcrypt_context, ALGORITHM, SECRET_KEY, ADMIN_LIST
from core.database import database_dependens
from jose import jwt
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


def create_or_update_user(new_info, old_info=None, created=True):
    if created:
        for fields, value in new_info.model_dump().items():
            setattr(old_info, fields, value)

    else:
        user = User(
            email=new_info.email,
            first_name=new_info.first_name.capitalize(),
            last_name=new_info.last_name.capitalize(),
            role=new_info.role,
            hashed_password=bcrypt_context.hash(new_info.password),
        )

        return user


def check_role(user_id, db: database_dependens):
    user = db.query(User).get(user_id)

    if user is None or user.role not in ADMIN_LIST:
        raise HTTPException(
            status_code=401, detail="You don't have permission for this"
        )

    return True
