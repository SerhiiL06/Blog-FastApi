from fastapi import FastAPI

from src.auth import routers, admin
from src.blog.routers import blog_router
from src.blog.admin import admin_post_router
from src.comments.routers import comments_router
from src.auth.models import User
from src.blog.models import Category, Post

from src.comments.models import Comment
from core.database import Base, engine


Base.metadata.create_all(engine)

app = FastAPI()


app.include_router(routers.auth_router)
app.include_router(admin.admin_auth_router)
app.include_router(blog_router)
app.include_router(admin_post_router)
app.include_router(comments_router)
