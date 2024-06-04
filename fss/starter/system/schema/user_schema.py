"""User domain schema"""

from pydantic import BaseModel, field_validator
from sqlmodel import Field


class UserCreateCmd(BaseModel):
    """
    UserCreate schema
    """

    username: str = Field(..., min_length=2, max_length=32)
    password: str = Field(..., min_length=6, max_length=64)
    nickname: str = Field(..., min_length=2, max_length=32)

    @field_validator("password")
    def password_complexity(cls, value):
        """
        Add your verification rules here
        """
        return value


class UserQuery(BaseModel):
    """
    UserQuery schema
    """

    id: int
    username: str
    nickname: str


class LoginCmd(BaseModel):
    """
    Login schema
    """

    username: str
    password: str


class UpdateUserCmd(BaseModel):
    """
    Update user schema
    """

    id: int
    nickname: str


class UserExport(BaseModel):
    """
    UserExport schema
    """

    username: str
    password: str
    nickname: str
