from fastapi import APIRouter, Depends, HTTPException
from core.database import SessionLocal, database_dependens
from src.auth.utils import current_user
from src.auth.logic import check_role
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


@blog_router.get("/single_post/{post_id}", response_model=PostReadScheme)
async def single_post(post_id: int, db: database_dependens):
    post = db.query(Post).get(post_id)
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
