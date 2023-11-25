from pydantic import BaseModel, ConfigDict, EmailStr, Field
from typing import Optional
from datetime import datetime


class UserScheme(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    email: EmailStr
    first_name: str
    last_name: str


class UserCreateScheme(UserScheme):
    role: Optional[str] = Field(default="user")
    password: str = Field(pattern="[A-Za-z0-9]{5,}")


class UserReadScheme(UserScheme):
    is_active: bool = Field(default=True)
    join_at: datetime


class ChangePasswordScheme(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    old_password: str
    new_password: str = Field(pattern="[A-Za-z0-9]{5,}")
