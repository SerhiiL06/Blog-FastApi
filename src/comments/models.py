from sqlalchemy import Column, String, Integer, DateTime, ForeignKey
from core.database import Base
from datetime import datetime


class Comment(Base):
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True, index=True)
    text = Column(String(100))
    created = Column(DateTime, default=datetime.now)

    user = Column(Integer, ForeignKey("users.id"))
    post = Column(Integer, ForeignKey("posts.id"))
