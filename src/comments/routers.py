from fastapi import APIRouter, HTTPException, Depends
from core.database import database_dependens

from src.auth.utils import current_user
from src.auth.models import User

from fastapi_mail import MessageSchema, FastMail
from config import MAIL_CONFIG
from typing import Annotated

from src.blog.models import Post
from .schemes import CommentScheme, ReadCommentScheme, SendEmailScheme
from .models import Comment
from .logic import do_comment


comments_router = APIRouter(prefix="/comments", tags=["comments"])


@comments_router.post("/add-comment/{post_id}", response_model=ReadCommentScheme)
async def create_comment(
    post_id: int, new_comment: CommentScheme, user: current_user, db: database_dependens
):
    if not user:
        raise HTTPException(status_code=401, detail="You need authorization")

    post = db.query(Post).get(post_id)

    if post is None:
        raise HTTPException(status_code=204, detail="Post doesnt exists")

    comment = Comment(
        **new_comment.model_dump(), post=post_id, user=user.get("user_id")
    )

    db.add(comment)
    db.commit()
    return comment


@comments_router.get("/all-comments")
async def get_comments(db: database_dependens, filter: str = None):
    return db.query(Comment).all()


@comments_router.patch("/{comment_id}")
async def update_comment(
    comment_id: int,
    user: current_user,
    db: database_dependens,
    current_comment: CommentScheme,
):
    return do_comment(
        comment_id=comment_id,
        user=user,
        db=db,
        comment_text=current_comment,
        update=True,
    )


@comments_router.delete("/{comment_id}")
async def delete_comment(comment_id: int, user: current_user, db: database_dependens):
    return do_comment(comment_id=comment_id, user=user, db=db)


@comments_router.post("/send-email/{user_id}")
async def send_email(message: SendEmailScheme, db: database_dependens, user_id: int):
    email = FastMail(MAIL_CONFIG)

    recipient = db.query(User).get(user_id)

    if not recipient:
        raise HTTPException(status_code=204, detail="user doesnt exists")

    msg = MessageSchema(
        recipients=[recipient.email],
        subject=message.subject,
        body=message.text,
        subtype="html",
    )

    await email.send_message(message=msg)

    return "Message was sent"
