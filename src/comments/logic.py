from fastapi import HTTPException
from fastapi.responses import JSONResponse
from .schemes import CommentScheme
from .models import Comment
from src.auth.logic import check_role
from src.auth.utils import current_user
from core.database import database_dependens


def do_comment(comment_id, user, db, comment_text: CommentScheme = None, update=None):
    comment = db.query(Comment).get(comment_id)

    if not comment:
        raise HTTPException(status_code=204, detail="something went wrong")

    if not check_role(user.get("user_id"), db) and (
        comment.user != user.get("user_id")
    ):
        raise HTTPException(status_code=401, detail="you dont have permission for this")

    if update is None:
        db.delete(comment)
        db.commit()
        return JSONResponse(content="You delete comment", status_code=200)

    comment.text = comment_text.text

    db.commit()
    return "Comment was update"
