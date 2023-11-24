from pydantic import Field, BaseModel, ConfigDict
from typing import Optional


class CategoryScheme(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    title: str = Field(max_length=50)


class ReadCategoryScheme(CategoryScheme):
    id: int


class PostScheme(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    title: str = Field(max_length=50)
    text: Optional[str] = None


class PostCreateScheme(PostScheme):
    category: int


class PostUpdateScheme(PostScheme):
    is_published: Optional[bool] = True


class PostReadScheme(PostUpdateScheme):
    id: int
    owner: int
    category: int
