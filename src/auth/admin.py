from fastapi import APIRouter
from fastapi.responses import JSONResponse

from .schemes import UserReadScheme
from .utils import current_user
from .exceptions import user_dont_exists
from config import ADMIN_LIST
from .logic import check_role
from .models import User
from core.database import database_dependens


admin_auth_router = APIRouter(prefix="/admin", tags=["admin auth"])


@admin_auth_router.get("/user-list", response_model=list[UserReadScheme])
async def user_list(user: current_user, db: database_dependens):
    check_role(user_id=user.get("user_id"), db=db)

    return db.query(User).all()


@admin_auth_router.delete("/delete-user/{user_id}")
async def delete_user(user_id: int, db: database_dependens, user: current_user):
    check_role(user_id=user.get("user_id"), db=db)

    user = db.query(User).get(user_id)

    if user is None:
        raise user_dont_exists()

    db.delete(user)

    db.commit()

    return JSONResponse(content="You delete user", status_code=200)
