from core.database import database_dependens
from src.auth.utils import current_user
from src.auth.logic import check_role
from src.auth.models import User
from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from .logic import update_post_fields
from .models import Post
from .schemes import PostUpdateScheme, PostReadScheme

admin_post_router = APIRouter(prefix="/blog/admin", tags=["blog admin"])


@admin_post_router.patch("/{post_id}", response_model=PostReadScheme)
async def update_post(
    post_id: int,
    post_info: PostUpdateScheme,
    user: current_user,
    db: database_dependens,
):
    check_role(user.get("user_id"), db)

    post = db.uquery(Post).get(post_id)

    if not post:
        raise HTTPException("Post doesnt exists")

    update_post_fields(post, post_info)

    db.commit()

    return post


@admin_post_router.delete("/{post_id}")
async def delete_post(post_id: int, user: current_user, db: database_dependens):
    check_role(user.get("user_id"), db)

    post = db.uquery(Post).get(post_id)

    if not post:
        raise HTTPException("Post doesnt exists")

    db.delete(post)
    db.commit()

    return JSONResponse(content="Well done", status_code=200)
