from core.database import Base
from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime


class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True)
    title = Column(String(50))

    posts = relationship("Post")


class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True)
    title = Column(String(150))

    text = Column(String(500), nullable=True)
    created = Column(DateTime, default=datetime.now)
    is_published = Column(Boolean, default=True)

    owner = Column(Integer, ForeignKey("users.id"))
    category = Column(Integer, ForeignKey("categories.id"))
