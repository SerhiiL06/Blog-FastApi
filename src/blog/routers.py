from fastapi import APIRouter, Depends, HTTPException, Response
from fastapi_mail import FastMail, MessageSchema
from typing import Annotated, List
from config import MAIL_CONFIG
from core.database import database_dependens
from src.auth.utils import current_user
from src.auth.logic import check_role
from src.auth.models import User
from .models import Category, Post, Bookmark
from .logic import update_post_fields
from .schemes import (
    ReadCategoryScheme,
    CategoryScheme,
    PostCreateScheme,
    PostReadScheme,
    PostUpdateScheme,
    BookmarkScheme,
)


blog_router = APIRouter(prefix="/blog", tags=["blog"])


@blog_router.get("/category-list")
async def category_list(db: database_dependens):
    return db.query(Category).all()


@blog_router.get("/category/{category_id}", response_model=ReadCategoryScheme)
async def get_category(category_id: int, db: database_dependens):
    category = db.query(Category).get(category_id)

    if not category:
        raise HTTPException(status_code=204, detail="Category doesnt exists")

    return category


@blog_router.post("/create-category", response_model=ReadCategoryScheme)
async def create_category(
    category: CategoryScheme, user: current_user, db: database_dependens
):
    check_role(user.get("user_id"), db)

    new_category = Category(**category.model_dump())
    db.add(new_category)
    db.commit()

    return new_category


@blog_router.get("/post-list")
async def post_list(db: database_dependens):
    return db.query(Post).all()


@blog_router.get("/single_post/{post_id}", response_model=list[PostReadScheme])
async def single_post(post_id: int, db: database_dependens):
    post = db.query(Post).join(Post.comments).all()
    if not post:
        return HTTPException(status_code=204, detail="Post doesnt exists")

    return post


@blog_router.get("/my-posts", response_model=list[PostReadScheme])
async def get_my_post(user: current_user, db: database_dependens):
    if not current_user:
        raise HTTPException(status_code=401, detail="Authorizate please")
    my_posts = db.query(Post).filter(Post.owner == user.get("user_id")).all()
    return my_posts


@blog_router.post("/create-post", response_model=PostReadScheme)
async def post_list(
    post: PostCreateScheme,
    current_user: current_user,
    db: database_dependens,
):
    if not current_user:
        return HTTPException(status_code=401, detail="you must authorization")

    new_post = Post(**post.model_dump(), owner=current_user.get("user_id"))

    db.add(new_post)
    db.commit()

    html = (
        f"""<p>Hi this test mail, thanks for using Fastapi-mail {new_post.text}</p> """
    )

    message = MessageSchema(
        recipients=[current_user.get("email")],
        subject="Hello",
        subtype="html",
        body=html,
    )

    email = FastMail(MAIL_CONFIG)

    await email.send_message(message=message)

    return new_post


@blog_router.delete("/delete-post/{post_id}")
async def post_list(post_id: int, user: current_user, db: database_dependens):
    post = db.query(Post).get(post_id)
    if not post:
        return HTTPException(status_code=204, detail="Post doesnt exists")

    if post.owner.id != user.get("user_id"):
        raise HTTPException(status_code=401, detail="you can delete only your posts")

    db.delete(post)
    db.commit()

    return "Post was deleted"


@blog_router.patch("/update-post/{post_id}", response_model=PostReadScheme)
async def update_post(
    post_id: int,
    update_info: PostUpdateScheme,
    user: current_user,
    db: database_dependens,
):
    post = db.query(Post).get(post_id)

    if not post:
        return HTTPException(status_code=204, detail="Post doesnt exists")

    if post.owner != user.get("user_id"):
        raise HTTPException(status_code=401, detail="you can delete only your posts")

    update_post_fields(post, update_info)

    db.commit()

    return post


@blog_router.get("/add-to-bookmark/{post_id}")
async def bookmarks(user: current_user, db: database_dependens, post_id: int):
    if not current_user:
        return HTTPException(status_code=401, detail="authorizate please")

    new_bookmark = (
        db.query(Bookmark)
        .filter(Bookmark.post == post_id, Bookmark.user == user.get("user_id"))
        .first()
    )

    if not new_bookmark:
        new_bookmark = Bookmark(post=post_id, user=user.get("user_id"))

        db.add(new_bookmark)

        db.commit()

        return Response(content="Well done!", status_code=200)

    db.delete(new_bookmark)

    db.commit()

    return Response(content="Bookmark was delete", status_code=200)


@blog_router.get("/my-bookmarks", response_model=list[PostReadScheme])
async def my_bookmarks(user: current_user, db: database_dependens):
    if not user:
        raise HTTPException(status_code=401, detail="auth please")
    posts = (
        db.query(Post)
        .join(Bookmark, Post.id == Bookmark.post)
        .filter(Bookmark.user == user.get("user_id"))
        .all()
    )

    return posts
