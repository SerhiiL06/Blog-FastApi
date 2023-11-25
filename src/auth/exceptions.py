from fastapi import HTTPException


def user_dont_exists():
    return HTTPException(status_code=401, detail="You don't have permission for this")
