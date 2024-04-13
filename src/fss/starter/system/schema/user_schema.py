"""User domain schema"""

from pydantic import BaseModel


class UserCreateCmd(BaseModel):
    """
    UserCreate schema
    """

    username: str
    password: str
    nickname: str


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
