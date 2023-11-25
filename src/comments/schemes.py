from pydantic import Field, BaseModel, ConfigDict
from src.auth.schemes import UserScheme
from datetime import datetime


class CommentScheme(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    text: str = Field(max_length=100)


class ReadCommentScheme(CommentScheme):
    id: int
    created: datetime

    user: int

    post: int
