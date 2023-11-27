from pydantic import Field, BaseModel, ConfigDict
from src.auth.schemes import UserScheme
from typing import Optional
from datetime import datetime


class CommentScheme(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    text: str = Field(max_length=100)


class ReadCommentScheme(CommentScheme):
    id: int
    created: datetime

    user: int

    post: int


class SendEmailScheme(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    subject: str = Field(max_length=150)
    text: Optional[str] = Field(max_length=250)
