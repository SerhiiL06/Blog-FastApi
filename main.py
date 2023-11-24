from fastapi import FastAPI

from src.auth.routers import auth_router
from src.blog.routers import blog_router
from src.auth.models import User
from src.blog.models import Category, Post
from core.database import Base, engine


Base.metadata.create_all(engine)

app = FastAPI()


app.include_router(auth_router)
app.include_router(blog_router)
