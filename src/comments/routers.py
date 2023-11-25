from fastapi import APIRouter, Depends, HTTPException, Query
from core.database import get_db, SessionLocal
from typing import Annotated
from src.auth.utils import get_current_user
from src.auth.models import User
from src.blog.models import Post
from .schemes import CommentScheme, ReadCommentScheme
from .models import Comment


comments_router = APIRouter(prefix="/comments", tags=["comments"])


@comments_router.post("/add-comment/{post_id}", response_model=ReadCommentScheme)
async def create_comment(
    post_id: int,
    new_comment: CommentScheme,
    current_user: dict = Depends(get_current_user),
    db: SessionLocal = Depends(get_db),
):
    post = db.query(Post).get(post_id)

    if post is None:
        raise HTTPException(status_code=204, detail="Post doesnt exists")

    comment = Comment(
        **new_comment.model_dump(), post=post_id, user=current_user.get("user_id")
    )

    db.add(comment)
    db.commit()
    return comment


@comments_router.get("/all-comments")
async def get_comments(
    db: Annotated[SessionLocal, Depends(get_db)], filter: str = None
):
    return db.query(Comment).all()
