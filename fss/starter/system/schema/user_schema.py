"""User domain schema"""

from pydantic import BaseModel


# UserCreate schema
class UserCreate(BaseModel):
    username: str
    password: str
    nickname: str


# UserQuery schema
class UserQuery(BaseModel):
    id: int
    username: str
    nickname: str
