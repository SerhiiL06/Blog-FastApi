from core.database import Base
from sqlalchemy import Column, Integer, String, Boolean, DateTime
from typing import Literal
from datetime import datetime


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String, unique=True)
    first_name = Column(String)
    last_name = Column(String)

    role = Column(String)

    join_at = Column(DateTime, default=datetime.now)
    is_active = Column(Boolean, default=True)

    hashed_password = Column(String)
