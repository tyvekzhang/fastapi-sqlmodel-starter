"""User entity"""

from typing import Optional

from sqlmodel import Field, Column, String, SQLModel

from src.main.app.common.entity.base_entity import ModelExt, BaseModel


class BaseUser(SQLModel):
    username: str = Field(sa_column=Column(String(32), index=True, unique=True, nullable=True, comment="用户名"))
    password: str = Field(default=None, sa_column=Column(String(64), nullable=True, comment="密码"))
    nickname: Optional[str] = Field(default=None, sa_column=Column(String(32), comment="昵称"))
    avatar: Optional[str] = Field(default=None, sa_column=Column(String(64), comment="头像"))


class UserEntity(ModelExt, BaseUser, BaseModel, table=True):
    __tablename__ = "sys_user"
    __table_args__ = {"comment": "用户信息表"}
