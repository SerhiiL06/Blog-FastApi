from fastapi import Depends, HTTPException
from datetime import datetime
from typing import Annotated

from jose import jwt, JWTError
from config import SECRET_KEY, ALGORITHM, bearer


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


current_user = Annotated[dict, Depends(get_current_user)]
