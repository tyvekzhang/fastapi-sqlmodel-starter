"""User domain schema"""

from pydantic import BaseModel


# UserCreate schema
class UserCreateCmd(BaseModel):
    username: str
    password: str
    nickname: str


# UserQuery schema
class UserQuery(BaseModel):
    id: int
    username: str
    nickname: str


# Login schema
class LoginCmd(BaseModel):
    username: str
    password: str
