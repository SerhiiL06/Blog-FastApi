from fastapi import APIRouter, Depends, HTTPException
from core.database import get_db, SessionLocal
from src.auth.utils import get_current_user
from .models import Category, Post
from .logic import update_post_fields
from .schemes import (
    ReadCategoryScheme,
    CategoryScheme,
    PostCreateScheme,
    PostReadScheme,
    PostUpdateScheme,
)


blog_router = APIRouter(prefix="/blog", tags=["blog"])


@blog_router.get("/category-list")
async def category_list(db: SessionLocal = Depends(get_db)):
    return db.query(Category).all()


@blog_router.get("/category/{category_id}", response_model=ReadCategoryScheme)
async def get_category(category_id: int, db: SessionLocal = Depends(get_db)):
    category = db.query(Category).get(category_id)

    if not category:
        raise HTTPException(status_code=204, detail="Category doesnt exists")

    return category


@blog_router.post("/create-category", response_model=ReadCategoryScheme)
async def create_category(category: CategoryScheme, db: SessionLocal = Depends(get_db)):
    new_category = Category(**category.model_dump())
    db.add(new_category)
    db.commit()

    return new_category


@blog_router.get("/post-list")
async def post_list(db: SessionLocal = Depends(get_db)):
    return db.query(Post).all()


@blog_router.get("/single_post/{post_id}", response_model=PostReadScheme)
async def single_post(post_id: int, db: SessionLocal = Depends(get_db)):
    post = db.query(Post).get(post_id)
    if not post:
        return HTTPException(status_code=204, detail="Post doesnt exists")

    return post


@blog_router.get("/my-posts", response_model=list[PostReadScheme])
async def get_my_post(
    current_user: dict = Depends(get_current_user), db: SessionLocal = Depends(get_db)
):
    my_posts = db.query(Post).filter(Post.owner == current_user.get("user_id")).all()
    return my_posts


@blog_router.post("/create-post", response_model=PostReadScheme)
async def post_list(
    post: PostCreateScheme,
    current_user: dict = Depends(get_current_user),
    db: SessionLocal = Depends(get_db),
):
    if not current_user:
        return HTTPException(status_code=401, detail="you must authorization")

    new_post = Post(**post.model_dump(), owner=current_user.get("user_id"))

    db.add(new_post)
    db.commit()

    return new_post


@blog_router.delete("/delete-post/{post_id}")
async def post_list(post_id: int, db: SessionLocal = Depends(get_db)):
    post = db.query(Post).get(post_id)
    if not post:
        return HTTPException(status_code=204, detail="Post doesnt exists")

    db.delete(post)
    db.commit()

    return "Post was deleted"


@blog_router.patch("/update-post/{post_id}", response_model=PostReadScheme)
async def update_post(
    post_id: int, update_info: PostUpdateScheme, db: SessionLocal = Depends(get_db)
):
    post = db.query(Post).get(post_id)

    if not post:
        return HTTPException(status_code=204, detail="Post doesnt exists")

    update_post_fields(post, update_info)

    db.commit()

    return post
